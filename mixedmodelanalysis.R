library(lme4)
#library(caret)
#setwd("/home/lindsey/Desktop/PythonFiles/Shams/Flashbeeps2.0")

foo <- read.delim("GLMMData_ecc.tsv",
                  colClasses=c(subjnum="numeric", cue_attn="numeric", blcnum="numeric",
                               trial_num="integer", condition_type="integer", flashed="integer",
                               number_pressed="numeric", raw_RT="numeric", control="numeric",
                               V1A1_or_V2A2="integer", V1A2="integer", V2A1="integer", Vcent="integer",
                               Vperiph_Af_center="integer", Vperiph_Af_periph="integer"))
# this set of condition codes comes from the magical python script
two_auditory_events_colocated_with_visual <- c(25, 13, 14, 26, 27, 15, 16, 28,
                                               29, 17, 18, 30, 7, 43, 44, 8, 9,
                                               45, 46, 10, 11, 47, 48, 12)
foo$two_sounds_at_target_location <- foo$condition_type %in% two_auditory_events_colocated_with_visual

# variable notation:
#
# V: The visual stimuli (visual flash(es))
# A: An auditory stimulus
# Ac: The auditory stimulus that is collocated with the visual flash(es)
# Af: The auditory stimulus that is not collocated (foil) with the visual flash(es)
# center/cent: This indicates that a stimulus was located in the central position (one of three positions)
# type: indicates whether an auditory stimulus was 'noise burst' or 'tone complex'

# variable descriptions:
#
# number_pressed: Subjects pressed either "1" or "2" to indicate the number of flashes that they saw
# cue_attn: indicates whether or not a visual cue appeared prior to trial indicating location of flash(es)
# V1A1_or_V2A2: (collocated controls) the instances wherein the number of visual events match the number of events in the collocated auditory stream.
#               For example: V1A1 indicates that there was one visual flash and the collocated auditory stimuli also had one beep
#                            V2A2 indicates that there were two visual flashes and the collocated auditory stimulus also had two beeps
# V1A2: (fission) One visual flash occurred while two auditory beeps occurred in the collocated auditory stream.
# V2A1: (fusion) Two visual flashes occurred while one auditory beep occurred in the collocated auditory stream.
# Vcent: The trials in which the visual flash(es) occured in the center location (meaning that the auditory stream that was NOT collocated could only be one space away)
# Vperiph_Af_center: "Near" trials in which the visual flash(es) occured in the peripheral location and that the auditory stream that was NOT collocated was one space away in the center position.
# Vperiph_Af_periph: "Far" trials in which the visual flash(es) occured in the peripheral location and that the auditory stream that was NOT collocated was two spaces away in the other peripheral position.
# Ac_type: Indicates if the illusion inducing auditory stream was either a tone or a noise burst

# remove unused columns

foo <- within(foo, {
  blcnum <- NULL
  #trial_num <- NULL  # WE MIGHT NEED THIS ONE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  condition_type <- NULL
  #flashed <- NULL
  control <- NULL
  timingcheck <- NULL
  collapsed_conditions <- NULL
  ## WE DON'T NEED THESE THREE BECAUSE WE HAVE ECC !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  Vcent <- NULL
  Vperiph_Af_center <- NULL
  Vperiph_Af_periph <- NULL
})


##############################
# code factors and contrasts #
##############################

foo <- within(foo, {
  subjnum <- factor(subjnum)
  #number_pressed <- factor(number_pressed)  # DANGER! DANGER! DANGER! DANGER!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  pressed_two <- as.integer(number_pressed == 2)  # new outcome variable !!!!!!!!!!!!!!!!!!!!!!!!!!
  presses_match_V <- with(foo, number_pressed == flashed)
  cue_attn <- factor(cue_attn)
  V1A1_or_V2A2 <- factor(V1A1_or_V2A2)
  V1A2 <- factor(V1A2)
  V2A1 <- factor(V2A1)
  #ecc <- factor(ecc, levels=c(0,1,2), labels=c("Vcent", "Vperiph_Af_center", "Vperiph_Af_periph"))
  ecc <- factor(ecc, levels=c(0,1,2), labels=c("flank", "near", "far"))
  #Vcent <- factor(Vcent)
  #Vperiph_Af_center <- factor(Vperiph_Af_center)
  #Vperiph_Af_periph <- factor(Vperiph_Af_periph)
  Ac_type <- factor(Ac_type)
})

# helmert for "ecc" and "far"
my.helmert <- matrix(c(-2/3, 1/3, 1/3, 0, -1/2, 1/2), ncol = 2)
# THIS MAKES CLEAR WHICH COLUMN OF HELMERT STANDS FOR WHICH CONTRAST.
# ecc_targ means the colocated V & A were in eccentric (not center) position
# far_foil means the target was eccentric AND the foil Aud stimulus was eccentric on the opposite side (nothing in center)
colnames(my.helmert) <- c("_noncentral_flash_loc", "_noncentral_flash_and_faraway_foil")
# assigning the new helmert coding to ecc
contrasts(foo$ecc) = my.helmert
#str(foo)

# A TABULATION SPLIT BY "CONTROL VS FISSION-INDUCING VS FUSION-INDUCING" !!!!!!!!!!!!!!!!!!!!!!
foo$condition_factor <- with(foo, ifelse(V1A2 == 1, "fission", ifelse(V2A1 == 1, "fusion", "control")))
thetable <- by(foo$presses_match_V, foo$condition_factor, function(i) {
  c(n_correct=sum(i), n_trials_of_this_type=length(i),
    pct_correct=100 * sum(i) / length(i))})
print(thetable)
############
# Modeling #
############

# null model:
#nul_mod <- glmer(presses_match_V ~ (1|subjnum), data=foo, family=binomial(link="probit"))
#summary(nul_mod)

# full model:
# deleted V1A1_or_V2A2 term (the control condition); the intercept term covers this case !!!!!!!!!!!!!!!!!
#ful_mod <- glmer(presses_match_V ~ cue_attn + V1A2 + V2A1 + Ac_type + ecc + (1|subjnum), data=foo, family=binomial(link="probit"))
#summary(ful_mod)

# model dropping Ac_type:
#drop1_mod <- glmer(presses_match_V ~ cue_attn + V1A2 + V2A1 + ecc + (1|subjnum), data=foo, family=binomial(link="probit"))
#summary(drop1_mod)

# THIS IS THE SIGNAL DETECTION THEORY STYLE MIXED MODEL !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
foo$two_flashes <- foo$flashed == 2  # this is the "truth" parameter
null_form <- formula(pressed_two ~ two_flashes + (1|subjnum))
full_form <- formula(pressed_two ~ two_flashes*cue_attn*ecc + 
                       two_flashes*two_sounds_at_target_location + (1|subjnum))
dprime_null_mod <- glmer(null_form, data=foo, family=binomial(link='probit'))
dprime_full_mod <- glmer(full_form, data=foo, family=binomial(link='probit'))
print(summary(dprime_null_mod))
print(summary(dprime_full_mod))  # convergence warning...
# ...removing the 3-way interaction:
reduced_form <- formula(pressed_two ~ two_flashes*cue_attn + two_flashes*ecc + 
                          two_flashes*two_sounds_at_target_location + (1|subjnum))
dprime_reduced_mod <- glmer(reduced_form, data=foo, family=binomial(link='probit'))
print(summary(dprime_reduced_mod))

# significantly better fit than null model?
anova(dprime_reduced_mod, dprime_null_mod)


# # get more info about the fit:
# confint(ful_mod)
# 
# # regression assumptions check:
# # http://tutorials.iq.harvard.edu/R/Rstatistics/Rstatistics.html
# par(mar = c(4, 4, 2, 2), mfrow = c(1, 2)) #optional
# plot(ful_mod, which = c(1, 2)) # "which" argument optional


