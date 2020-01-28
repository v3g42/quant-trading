function [p, settings] = trendfollowing(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings)
settings.markets     = {'CASH', 'F_AD', 'F_BO', 'F_BP', 'F_C', 'F_CC', 'F_CD', 'F_CL', 'F_CT', 'F_DX', 'F_EC', 'F_ED', 'F_ES', 'F_FC', 'F_FV', 'F_GC', 'F_HG', 'F_HO', 'F_JY', 'F_KC', 'F_LB', 'F_LC', 'F_LN', 'F_MD', 'F_MP', 'F_NG', 'F_NQ', 'F_NR', 'F_O', 'F_OJ', 'F_PA', 'F_PL', 'F_RB', 'F_RU', 'F_S', 'F_SB', 'F_SF', 'F_SI', 'F_SM', 'F_TU', 'F_TY', 'F_US', 'F_W', 'F_XX', 'F_YM'};
settings.sample1end   = 20121231;
settings.lookback    = 504;

if ~any(strcmp(fieldnames(settings), 'myField'))
    settings.myField = zeros(size(DATE));
end

settings.myField(end) = DATE(end);

nMarkets = size(CLOSE,2);
periodLonger   = 200; %#[150:10:200]#
periodShorter = 40;  %#[20:5:60]#

smaLongerPeriod   = sum(CLOSE(end-periodLonger+1:end,:)) / periodLonger;
smaShorterPeriod = sum(CLOSE(end-periodShorter+1:end,:)) / periodShorter;

long = smaShorterPeriod >= smaLongerPeriod;

p = zeros(1, nMarkets);
p(long)  = 1;
p(~long) = -1;

end
