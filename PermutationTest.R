rm(list=ls())
library(R.utils)
library(hash) ##to use 'dictionary' functionality 
library(dplyr)
library(lme4)
library(future.apply)
library(parallel)
library(ggplot2)
library(svglite)
suppressWarnings(library(lme4))
#path <- "/group/jbinder/work/songkim/Projects/VerbSpec_eelbrain27/singletrialexport_fixed/2_or_3_word_trials_subspecificity/LATP"
path <- "/group/jbinder/work/songkim/Projects/VerbSpec_eelbrain27/singletrialexport_fixed/2_or_3_word_trials_subspecificity/left_BA21"
setwd(path)
raw0 <- read.csv(file.path(path, "grand_ds"))
print('raw0 is read')
cond <- strsplit(path, "/")[[1]][9]
roi <- strsplit(path, "/")[[1]][10]

##########first reconstruct the grand-averaged data ############ 
# cols = c("index", "srcm_at_t", "t", "subject", "sub_specificity", "sentence")
# raw_mini <- raw0[, cols]
# raw_mini[["subject"]] <- as.factor(raw_mini[["subject"]])
# t_vec <- unique(raw_mini[['t']])
# 
# grand_avg_ts <- data.frame()
# for (i in t_vec) { ####t: from 0 to 400
#   raw_at_t <- subset(raw_mini, t==i)
#   print (dim(raw_at_t))
#   raw_at_t2 <- raw_at_t %>%
#     group_by(sub_specificity) %>% summarise(m=mean(srcm_at_t))
#   raw_at_t2$t <- i
#   grand_avg_ts <- rbind(grand_avg_ts, raw_at_t2)
#   print(dim(grand_avg_ts))
#   rm(raw_at_t2)
# }
# 
# #draw grand_avg_ts
# plot_title <- sprintf("grand average for %s", roi)
# 
# grand_ts_plot <- ggplot(data=grand_avg_ts, aes(x=t, y=m, group=sub_specificity)) +
#   geom_line(aes(color=sub_specificity))+ geom_point(aes(color=sub_specificity)) +
#   scale_x_continuous(breaks = seq(1, length(t_vec)-1, by = 5)) +
#   theme(axis.text.x = element_text(angle = 45, vjust = 0.5, size=10)) +
#   ggtitle(plot_title)
# ggsave("left_BA21.svg")
# ggsave("left_BA21.pdf")

############# define a generator of shuffled labels ###################
remap <- function(n) {
  pairs <- list(c(1,2,3), c(1,3,2), c(2,1,3), c(2,3,1), c(3,1,2), c(3,2,1))
  return (pairs[n])}

############ define a function that returns the biggest cluster for one permutation ################
findMaxCluster <- function(data, tstart, tstop) {
  p_vals <- numeric(0)
  chi_vals <- numeric(0)
  sig_times <- numeric(0)
  for (time in tstart:tstop) {
    df <- subset(data, t==time)
    m.full <- lmer(srcm_at_t ~ sub_specificity + freq_v + len_v + (1|subject), data=df, REML=FALSE)
    m.red <- lmer(srcm_at_t ~ freq_v + len_v + (1|subject), data=df, REML=FALSE)
    model_comp <- anova(m.full, m.red)
    if (model_comp$'Pr(>Chisq)'[2] <= 0.05) {
      sig_times <- c(sig_times, time)}
    
    p_vals <- c(p_vals, model_comp$'Pr(>Chisq)'[2])
    chi_vals <- c(chi_vals, model_comp$'Chisq'[2])
    #threshold <- qchisq(.95, df=model_comp$'Df'[2])
  }
  grouping <- split(sig_times, cumsum(c(1, diff(sig_times) != 1)))
  #print (grouping) ##3 clusters
  clusters <- numeric(length=length(grouping)) ##clusters=vector of chi-sums
  #print (clusters)
  for (i in 1:length(grouping)) {
    t_stretch <- grouping[[i]]
    cum_chi <- 0
    #print (c('group number', i))
    for (j in t_stretch) {
      cum_chi <- cum_chi + chi_vals[j-(tstart-1)]
    }
    clusters[i] <- cum_chi
  }
  
  ### save maximum chi_square and its time interval
  max_chi <- max(clusters) ##find the largest chisq value
  max_chi_idx <- match(max_chi, clusters) ###find its position in the vector
  max_chi_t <- grouping[[max_chi_idx]]
  returnlist <- list(max_chi_t, max_chi)
  names(returnlist) <- c("timepoints", "maxsumofChisq")
  return (returnlist)
}
print ('function definition finished')


##if to find the maximal cluster of original data
#res0 <- findMaxCluster(raw0, 181, 281)

######### define a function that returns p val from N permutation  #################

#datafile <- read.csv('2_or_3_word_trials_subspecificity/Frankland-25/grand_ds')
#datafile <- raw0
#print ('datafile reading is finished')

permutationTest <- function(dataframe, nperm, tstart, tstop) {
  print("permutation Test begins")
  #raw_orig <- read.csv(datafile)
  raw_orig <- dataframe
  col_to_select = c("index", "srcm_at_t", "t", "subject", "sub_specificity", "sentence",
                    "word1", "word2", "RT", "Nmorph_o", "Nmorph_s", "Nmorph_v", 
                    "combinatoriness", "freq_o", "freq_s", "freq_v", "len_o", "len_s", "len_v")
  raw_orig <- raw_orig[, col_to_select]
  factors <- c("subject", "sub_specificity", "sentence", "word1", "word2", "combinatoriness")
  for (f in factors) {
    raw_orig[[f]] <- as.factor(raw_orig[[f]])
  }
  raw_orig$sub_specificity <- recode_factor(raw_orig$sub_specificity, "general"="1", "specific"="2", "hashtag"="3")
  
  ### get max cluster for the actual data
  res_orig <- findMaxCluster(raw_orig, tstart, tstop)
  maxchi_observed <- res_orig[['maxsumofChisq']]
  
  ### create 10000 set of shuffled labels
  perm_dict <- hash()
  for (i in 1:nperm){
    nsubj = 27
    label_shuffle_ix <- sample(c(1:5), size=nsubj, replace=T)
    #v = np.random.randint(0,5,nsubj)
    
    one_perm_for_group <- vector(mode="list", length=nperm)
    for (ix in 1:length(label_shuffle_ix)) {
      one_perm_for_group[ix] <- remap(label_shuffle_ix[ix])
    }
    perm_dict[[as.character(i)]] <- one_perm_for_group
  }
  print ('perm_dict is created')
  
  ############# apply label permutation to data ###############
  # ind_data <- list.files(path)
  # ind_data <- ind_data[!startsWith(ind_data, 'grand')]
  #chisq_dist = vector(mode="integer", length=nperm)
  #plan(multiprocess)
  #teval(mclapply(tasks,solver,mc.cores=detectCores()))
  print ('mclapply starts')
  mc_start <- Sys.time()
  chisq_dist2 <- mclapply(seq(nperm), function(i) {
    #print(i)
    raw_perm <- raw_orig
    raw_perm$sub_specificity_perm <- raw_perm$sub_specificity
    subjlist <- levels(raw_perm$subject)
    for (j in 1:length(subjlist)) {
      raw_perm[raw_perm$subject == subjlist[j], ]$sub_specificity_perm <- 
        recode_factor(raw_perm[raw_perm$subject==subjlist[j], ]$sub_specificity_perm, 
                      "1"=perm_dict[[as.character(i)]][[j]][1], 
                      "2"=perm_dict[[as.character(i)]][[j]][2], 
                      "3"=perm_dict[[as.character(i)]][[j]][3])
      
    }
    ### drop the unshuffled sub_specificity column
    drops <- "sub_specificity"
    raw_perm <- raw_perm[, !names(raw_perm) %in% drops]
    raw_perm <- raw_perm %>% rename(sub_specificity = sub_specificity_perm)
    
    #### do the stat for the new shuffled df
    res_perm <- findMaxCluster(raw_perm, tstart, tstop)
    print(sprintf("%i: result is %s", i, res_perm["maxsumofChisq"]))
    maxChi_perm <- res_perm[['maxsumofChisq']]
    #chisq_dist[i] = maxChi_perm
    maxChi_perm
    
  }, mc.cores = 15
  )
  mc_finish <- Sys.time()
  mc_time <- mc_finish - mc_start
  print ('mclapply finished')
  print (mc_time)
  
  chi_larger_than_observed2 = sum(chisq_dist2 > maxchi_observed)
  pvalue = chi_larger_than_observed2 / nperm
  returnlist2 <- list(res_orig, unlist(chisq_dist2), pvalue)
  names(returnlist2) <- c("res_orig", "chisq_dist2", "pvalue")
  return (returnlist2)
}

start.time <- Sys.time()
res <- permutationTest(raw0, 1000, 181, 281)
end.time <- Sys.time()
time.taken <- end.time - start.time
printf("total time taken is: %s", time.taken)

print ('saving to file')
filename <- file.path(path, "perm1000_core10_result.txt")
sink(filename)
print(res)
print(time.taken)
sink()
print ('file saved')
