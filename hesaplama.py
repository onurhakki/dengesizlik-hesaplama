
def hesaplama(df, ptf, smf, do_orani = 0.2, dengesizlik_yuzde  = 0.03):
    df["EDM P (MWh)"] = (
        df[["UEVM (MWh)","GÖP SAM (MWh)", "GİPAM (MWh)", "KEYATM (MWh)",   "İA Alış (MWh)",]].sum(axis = 1) -
        df[["UEÇM (MWh)", "GÖP SSM (MWh)", "GİPSM (MWh)",  "İA Satış (MWh)", "KEYALM (MWh)",]].sum(axis = 1)
        ).apply(lambda x: x if x > 0 else 0)
    df["EDM N (MWh)"] = (
        df[["UEÇM (MWh)", "GÖP SSM (MWh)", "GİPSM (MWh)",  "İA Satış (MWh)", "KEYALM (MWh)",]].sum(axis = 1) -
        df[["UEVM (MWh)","GÖP SAM (MWh)", "GİPAM (MWh)", "KEYATM (MWh)",   "İA Alış (MWh)",]].sum(axis = 1) 
        ).apply(lambda x: x if x > 0 else 0)

    df["BEDM (MWh)"] = df["EDM P (MWh)"]  - df["EDM N (MWh)"] 


    df["TAM (MWh)"] = df[["GÖP SAM (MWh)", "GİPAM (MWh)", "KEYATM (MWh)",  "İA Alış (MWh)",]].sum(axis = 1)
    df["TSM (MWh)"] = df[["GÖP SSM (MWh)", "GİPSM (MWh)",  "İA Satış (MWh)", "KEYALM (MWh)",]].sum(axis = 1)

    df["NAM (MWh)"] = df["UEVM (MWh)"] + (df["TAM (MWh)"] - df["TSM (MWh)"]).apply(lambda x: x if x > 0 else 0)
    df["NSM (MWh)"] = df["UEÇM (MWh)"] + (df["TSM (MWh)"] - df["TAM (MWh)"]).apply(lambda x: x if x > 0 else 0)

    df["PH (MWh)"] = df[["NAM (MWh)", "NSM (MWh)"]].max(axis = 1)
    df["Hesaplanan DO (%)"] = 100*df["BEDM (MWh)"]/df["PH (MWh)"]


    new_df = df[["EDM P (MWh)", "EDM N (MWh)","BEDM (MWh)", "TAM (MWh)", "TSM (MWh)", "NAM (MWh)", "NSM (MWh)", "PH (MWh)", "Hesaplanan DO (%)"]].copy()

    new_df["İzin Verilen Sinerji (MWh)"] = new_df["PH (MWh)"]*do_orani

    new_df["Ceza Durumu"] = new_df["İzin Verilen Sinerji (MWh)"] < new_df[["EDM P (MWh)", "EDM N (MWh)"]].sum(axis=1)
    new_df["Sinerji (MWh)"] = ~new_df["Ceza Durumu"]*(new_df["EDM P (MWh)"]-new_df["EDM N (MWh)"]) + new_df["Ceza Durumu"]*(new_df["İzin Verilen Sinerji (MWh)"])*((new_df["EDM P (MWh)"]-new_df["EDM N (MWh)"]).apply(lambda x: -1 if x < 0 else 1))

    new_df["Cezalı Sinerji (MWh)"] = new_df["Ceza Durumu"]*(
        ((new_df["EDM P (MWh)"]+new_df["EDM N (MWh)"])-new_df["İzin Verilen Sinerji (MWh)"])*
        ((new_df["EDM P (MWh)"]-new_df["EDM N (MWh)"]).apply(lambda x: -1 if x < 0 else 1)))

    new_df["Negatif Cezalı Sinerji (TL)"] = (new_df["Cezalı Sinerji (MWh)"]*(max(ptf,smf)*(1+dengesizlik_yuzde))).apply(lambda x: x if x < 0 else 0)
    new_df["Pozitif Cezalı Sinerji (TL)"] = (new_df["Cezalı Sinerji (MWh)"]*(min(ptf,smf)*(1-dengesizlik_yuzde))).apply(lambda x: x if x > 0 else 0)
    for i in new_df:
        new_df[i] = new_df[i].astype(float)
    return new_df
