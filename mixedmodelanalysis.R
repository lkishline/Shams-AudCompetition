library(lme4)
setwd("/home/lindsey/Desktop/PythonFiles/Shams/Flashbeeps2.0")

foo <- read.delim("GLMMData_ecc.tsv",
                 colClasses=c(subjnum="numeric", cue_attn="numeric", blcnum="numeric",
                              trial_num="integer", condition_type="character", flashed="integer",
                              number_pressed="numeric", raw_RT="numeric", control="numeric",
                              V1A1_or_V2A2="integer", V1A2="integer", V2A1="integer", Vcent="integer",
                              Vperiph_Af_center="integer", Vperiph_Af_periph="integer"))

# remove unused columns

foo <- within(foo, {
  blcnum <- NULL
  trial_num <- NULL
  condition_type <- NULL
  flashed <- NULL
  control <- NULL
  timingcheck <- NULL
  collapsed_conditions <- NULL
})


##############################
# code factors and contrasts #
##############################

foo <- within(foo, {
   subjnum <- factor(subjnum)
   number_pressed <- factor(number_pressed)
   cue_attn <- factor(cue_attn)
   V1A1_or_V2A2 <- factor(V1A1_or_V2A2)
   V1A2 <- factor(V1A2)
   V2A1 <- factor(V2A1)
   ecc <- factor(ecc, levels=c(0,1,2), labels=c("Vcent", "Vperiph_Af_center", "Vperiph_Af_periph"))
   Vcent <- factor(Vcent)
   Vperiph_Af_center <- factor(Vperiph_Af_center)
   Vperiph_Af_periph <- factor(Vperiph_Af_periph)
   Ac_type <- factor(Ac_type)
 })

# helmert for "ecc" and "far"
my.helmert = matrix(c(-2/3, 1/3, 1/3, 0, -1/2, 1/2), ncol = 2)
# assigning the new helmert coding to ecc
contrasts(foo$ecc) = my.helmert
str(foo)

############
# Modeling #
############

# null model:
nul_mod <- glmer(number_pressed ~ (1|subjnum), data=foo, family=binomial(link="probit"))
summary(nul_mod)

# full model:
ful_mod <- glmer(number_pressed ~ cue_attn + V1A1_or_V2A2 + V1A2 + V2A1 + Ac_type + ecc + (1|subjnum), data=foo, family=binomial(link="probit"))
summary(ful_mod)

# model dropping Ac_type:
drop1_mod <- glmer(number_pressed ~ cue_attn + V1A1_or_V2A2 + V1A2 + V2A1 + ecc + (1|subjnum), data=foo, family=binomial(link="probit"))
summary(drop1_mod)





# # get more info about the fit:
# confint(ful_mod)
# 
# # regression assumptions check:
# # http://tutorials.iq.harvard.edu/R/Rstatistics/Rstatistics.html
# par(mar = c(4, 4, 2, 2), mfrow = c(1, 2)) #optional
# plot(ful_mod, which = c(1, 2)) # "which" argument optional


