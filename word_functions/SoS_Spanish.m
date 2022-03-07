% Example name: VWFA_sos_v02
% This script was launched from within the python script, unless it is not working and then I should run it from the sos_gui() in matlab, select Create Plots and click in OPTIMIZE to check what it's going on. 
% All options have to be added here in the script (mainly the soft constraints and the statistical tests)
clear all; close all; clc;
% addpath('/bcbl/home/home_g-m/glerma/00local/PROYECTOS/VWFA/Stimuli/SoS');

% Sets the random seed
rng(3456,'twister');

bdir = fullfile(vlRP,'DATA');
odir = fullfile(bdir,'output');

%% Creates LF (0.5-10) and HF (100-300) populations from the espal 4-5 length database (it only reads the files already generated in Python script calling this script)
% LF_Population = population('espal456LF.txt','name','myPopulation','isHeader',true,'isFormatting',true);
% HF_Population = population('espal456HF.txt','name','myPopulation','isHeader',true,'isFormatting',true);
AllPop = population(fullfile(bdir,'Espal456SinCognados_SinConcreteness_UTF8.txt'),'name','myPopulation','isHeader',true,'isFormatting',true);

% Creates a second sample with 100 words that can be saved with the name 'mySample2.txt'
SampleLF1 = sample(80,'name','SampleLF1','outFile','RW_LF1Length456_80.txt');
SampleLF2 = sample(80,'name','SampleLF2','outFile','RW_LF2Length456_80.txt');
SampleHF1 = sample(80,'name','SampleHF1','outFile','RW_HF1Length456_80.txt');
SampleHF2 = sample(80,'name','SampleHF2','outFile','RW_HF2Length456_80.txt');

% Links Samples to the population file from which its items will be drawn
SampleLF1.setPop(LF_Population);
SampleLF2.setPop(LF_Population);
SampleHF1.setPop(HF_Population);
SampleHF2.setPop(HF_Population);

% Creates an SOS optimization called 'mySOS'
mySOS = sos();

% Adds the two samples to the 'mySOS' instance of optimization
mySOS = mySOS.addSample(SampleLF1);
mySOS = mySOS.addSample(SampleLF2);
mySOS = mySOS.addSample(SampleHF1);
mySOS = mySOS.addSample(SampleHF2);

% CREATE CONSTRAINTS
% Adds one desired constraint with the name 'C_'
% C1 = Match the two lists on 'frq'
C_frq_LF = mySOS.addConstraint('sosObj', mySOS, 'name','C_frq_LF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleLF1, 'sample2', SampleLF2, 's1ColName', 'frq', 'S2ColName', 'frq', 'exponent', 2, 'paired', false, 'weight', 1);
C_frq_HF = mySOS.addConstraint('sosObj', mySOS, 'name','C_frq_HF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleHF1, 'sample2', SampleHF2, 's1ColName', 'frq', 'S2ColName', 'frq', 'exponent', 2, 'paired', false, 'weight', 1);

% C2 = Match the two lists on 'nlet'
C_nlet_LF = mySOS.addConstraint('sosObj', mySOS, 'name','C_nlet_LF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleLF1, 'sample2', SampleLF2, 's1ColName', 'nlet', 'S2ColName', 'nlet', 'exponent', 2, 'paired', false, 'weight', 1);
C_nlet_HF = mySOS.addConstraint('sosObj', mySOS, 'name','C_nlet_HF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleHF1, 'sample2', SampleHF2, 's1ColName', 'nlet', 'S2ColName', 'nlet', 'exponent', 2, 'paired', false, 'weight', 1);
C_nlet_LHF = mySOS.addConstraint('sosObj', mySOS, 'name','C_nlet_LHF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleHF1, 'sample2', SampleLF1, 's1ColName', 'nlet', 'S2ColName', 'nlet', 'exponent', 2, 'paired', false, 'weight', 1);


% C3 = Match the two lists on 'conc'
% C_conc_LF = mySOS.addConstraint('sosObj', mySOS, 'name','C_conc_LF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleLF1, 'sample2', SampleLF2, 's1ColName', 'conc', 'S2ColName', 'conc', 'exponent', 2, 'paired', false, 'weight', 1);
% C_conc_HF = mySOS.addConstraint('sosObj', mySOS, 'name','C_conc_HF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleHF1, 'sample2', SampleHF2, 's1ColName', 'conc', 'S2ColName', 'conc', 'exponent', 2, 'paired', false, 'weight', 1);
% C_conc_LHF = mySOS.addConstraint('sosObj', mySOS, 'name','C_conc_LHF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleHF1, 'sample2', SampleLF1, 's1ColName', 'conc', 'S2ColName', 'conc', 'exponent', 2, 'paired', false, 'weight', 1);


% C4 = Match the two lists on 'Lev'
C_Lev_LF = mySOS.addConstraint('sosObj', mySOS, 'name','C_Lev_LF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleLF1, 'sample2', SampleLF2, 's1ColName', 'Lev', 'S2ColName', 'Lev', 'exponent', 2, 'paired', false, 'weight', 1);
C_Lev_HF = mySOS.addConstraint('sosObj', mySOS, 'name','C_Lev_HF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleHF1, 'sample2', SampleHF2, 's1ColName', 'Lev', 'S2ColName', 'Lev', 'exponent', 2, 'paired', false, 'weight', 1);
C_Lev_LHF = mySOS.addConstraint('sosObj', mySOS, 'name','C_Lev_LHF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleHF1, 'sample2', SampleLF1, 's1ColName', 'Lev', 'S2ColName', 'Lev', 'exponent', 2, 'paired', false, 'weight', 1);


% C5 = Match the two lists on 'bi'
C_bi_LF = mySOS.addConstraint('sosObj', mySOS, 'name','C_bi_LF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleLF1, 'sample2', SampleLF2, 's1ColName', 'bi', 'S2ColName', 'bi', 'exponent', 2, 'paired', false, 'weight', 1);
C_bi_HF = mySOS.addConstraint('sosObj', mySOS, 'name','C_bi_HF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleHF1, 'sample2', SampleHF2, 's1ColName', 'bi', 'S2ColName', 'bi', 'exponent', 2, 'paired', false, 'weight', 1);
C_bi_LHF = mySOS.addConstraint('sosObj', mySOS, 'name','C_bi_LHF', 'constraintType', 'soft', 'fnc', 'min', 'stat', 'mean', 'sample1', SampleHF1, 'sample2', SampleLF1, 's1ColName', 'bi', 'S2ColName', 'bi', 'exponent', 2, 'paired', false, 'weight', 1);




% Fills the two samples with randomly selected items from the population file
mySOS.initFillSamples();

% Standardizes the values of the dimension(s) of interest
mySOS.normalizeData();

% Creates an independent samples t-test to determine whether or not the lists are matched on 'frequency', p-value > 0.5
mySOS.addttest('name','myTTestHF','type','independent', 'sample1', SampleHF1, 'sample2', SampleHF2, 's1ColName', 'frq', 's2ColName', 'frq', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);
mySOS.addttest('name','myTTestLF','type','independent', 'sample1', SampleLF1, 'sample2', SampleLF2, 's1ColName', 'frq', 's2ColName', 'frq', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);

% Creates an independent samples t-test to determine whether or not the lists are matched on 'nlet', p-value > 0.5
mySOS.addttest('name','nletmyTTestHF','type','independent', 'sample1', SampleHF1, 'sample2', SampleHF2, 's1ColName', 'nlet', 's2ColName', 'nlet', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);
mySOS.addttest('name','nletmyTTestLF','type','independent', 'sample1', SampleLF1, 'sample2', SampleLF2, 's1ColName', 'nlet', 's2ColName', 'nlet', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);
mySOS.addttest('name','nletmyTTestLHF','type','independent', 'sample1', SampleLF1, 'sample2', SampleHF1, 's1ColName', 'nlet', 's2ColName', 'nlet', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);

% Creates an independent samples t-test to determine whether or not the lists are matched on 'conc', p-value > 0.5
% mySOS.addttest('name','concmyTTestHF','type','independent', 'sample1', SampleHF1, 'sample2', SampleHF2, 's1ColName', 'conc', 's2ColName', 'conc', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);
% mySOS.addttest('name','concmyTTestLF','type','independent', 'sample1', SampleLF1, 'sample2', SampleLF2, 's1ColName', 'conc', 's2ColName', 'conc', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);
% mySOS.addttest('name','concmyTTestLHF','type','independent', 'sample1', SampleLF1, 'sample2', SampleHF1, 's1ColName', 'conc', 's2ColName', 'conc', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);


% Creates an independent samples t-test to determine whether or not the lists are matched on 'Lev', p-value > 0.5
mySOS.addttest('name','LevmyTTestHF','type','independent', 'sample1', SampleHF1, 'sample2', SampleHF2, 's1ColName', 'Lev', 's2ColName', 'Lev', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);
mySOS.addttest('name','LevmyTTestLF','type','independent', 'sample1', SampleLF1, 'sample2', SampleLF2, 's1ColName', 'Lev', 's2ColName', 'Lev', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);
mySOS.addttest('name','LevmyTTestLHF','type','independent', 'sample1', SampleLF1, 'sample2', SampleHF1, 's1ColName', 'Lev', 's2ColName', 'Lev', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);

% Creates an independent samples t-test to determine whether or not the lists are matched on 'bi', p-value > 0.5
mySOS.addttest('name','bimyTTestHF','type','independent', 'sample1', SampleHF1, 'sample2', SampleHF2, 's1ColName', 'bi', 's2ColName', 'bi', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);
mySOS.addttest('name','bimyTTestLF','type','independent', 'sample1', SampleLF1, 'sample2', SampleLF2, 's1ColName', 'bi', 's2ColName', 'bi', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);
mySOS.addttest('name','bimyTTestLHF','type','independent', 'sample1', SampleLF1, 'sample2', SampleHF1, 's1ColName', 'bi', 's2ColName', 'bi', 'desiredpvalCondition', '=>', 'desiredpval', 0.5);

% Determines the type of optimization that will be performed; no specification defaults to "greedy"
%mySOS.setAnnealSchedule('schedule','exp');

% Starts the SOS GUI
% sos_gui();

% Starts the optimization process automatically
mySOS.optimize('isGui',0);


% Write Sample data files
SampleLF1.writeData();
SampleLF2.writeData();
SampleHF1.writeData();
SampleHF2.writeData();

% Quit Matlab, we call this script from a Python script
exit

