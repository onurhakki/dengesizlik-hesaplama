import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from hesaplama import hesaplama
st.set_page_config(
    page_title="Dengesizlik",
    page_icon=":bar_chart:",
    layout="wide",
)

ptf = st.sidebar.number_input("PTF (TL/MWh)", 0,3000,2000,1)
smf = st.sidebar.number_input("SMF (TL/MWh)", 0, 3000, 1000,1)
do_orani = 0.2, 
dengesizlik_yuzde = 0.03

columns = [
    "Org. ID",
    "UEVM (MWh)", "UEÇM (MWh)",
    "GÖP SAM (MWh)", "GÖP SSM (MWh)",
    "GİPAM (MWh)", "GİPSM (MWh)",
    "VEPAM (MWh)", "VEPSM (MWh)",
    "İA Alış (MWh)", "İA Satış (MWh)",
    "KEYALM (MWh)", "KEYATM (MWh)",
]

st.markdown("## Dengesizlik Hesaplama")

st.write("Yönetmelik değişikliği kapsamında dengeden sorumlu grup içerisindeki dengesizliklerin hesaplanmasına ilişkin iki yöntemin kıyaslanması gerçekleştirilmektedir. Bir saat için PTF ve SMF değerleri soldaki menüden belirlenebilir. Dengeden sorumlu grup içerisindeki piyasa katılımcılarının (maksimum 10 adet piyasa katılımcısı için) hacimleri Excel dosyası ile eklenmelidir.")
st.write("Örnek Excel dosyasına [linkten](https://github.com/onurhakki/dengesizlik-hesaplama/raw/main/Dengesizlik%20Hesaplama.xlsx) ulaşabilirsiniz. Sonrasında dosyayı yüklediğinizde dengesizlik sonuçlarını görebileceksiniz.")

st.markdown("### Dosya Yükleme")

check_error = False
uploaded_file = st.file_uploader("Dosya Seçiniz")


if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)[columns].iloc[:10].set_index("Org. ID").fillna(0)
        with st.expander("Yüklenen Excel"):
            st.write("Hücreye çift tıkladığınızda değerlerde değişiklik yapabilirsiniz.")
            df = st.data_editor(df, use_container_width=True)
            st.write("""
    - UEVM: uzlaştırmaya esas veriş miktarı (MWh),
    - UEÇM: uzlaştırmaya esas çekiş miktarı (MWh),
    - GÖP SAM: gün öncesi piyasında gerçekleştirmiş olduğu toplam alış miktarını (MWh),
    - GÖP SSM: gün öncesi piyasında gerçekleştirmiş olduğu toplam satış miktarını (MWh),
    - GİPAM: gün içi piyasında gerçekleştirmiş olduğu toplam alış miktarını (MWh),
    - GİPSM: gün içi piyasında gerçekleştirmiş olduğu toplam satış miktarını (MWh),
    - VEPAM: vadeli elektrik piyasında gerçekleştirmiş olduğu toplam alış miktarını (MWh),
    - VEPSM: vadeli elektrik piyasında gerçekleştirmiş olduğu toplam satış miktarını (MWh),
    - İA Alış: Uzlaştırmaya Esas İkili Anlaşma Alış Miktarını (MWh),
    - İA Satış: Uzlaştırmaya Esas İkili Anlaşma Satış Miktarını (MWh),
    - KEYALM: dengeleme güç piyasasındaki toplam Kabul Edilen ve Yerine Getirilmiş Yük Alma Teklifi Miktarını (MWh)
    - KEYATM: dengeleme güç piyasasındaki toplam Kabul Edilen ve Yerine Getirilmiş Yük Atma Teklifi Miktarını (MWh)

    """)
        check_error = True
    except:
        st.error("Hata: Excel dosyası hatalı. Lütfen örnek Excel dosyasını kullanınız.")
        check_error = False


st.divider()
st.markdown("### Sonuçlar")

if uploaded_file is not None and check_error == True:
    hesaplanan = hesaplama(df, ptf, smf, do_orani, dengesizlik_yuzde)

    with st.expander("Toplu Detaylar"):
        st.dataframe(hesaplanan.style.format(precision=2,thousands=".",decimal="."), use_container_width=True)
        st.write("""
 - EDM P: enerji dengesizliğinin giderilmesine yönelik sisteme sattığı enerji miktarını (MWh),
 - EDM P: enerji dengesizliğinin giderilmesine yönelik sistemden aldığı enerji miktarını (MWh),
 - BEDM: dengesizlik oranı tespitinde kullanılan bireysel enerji dengesizlik miktarını (MWh,
 - TAM: vadeli elektrik piyasası, gün öncesi piyasası, gün içi piyasası alışları ile uzlaştırmaya esas ikili anlaşma alış miktarları ve dengeleme güç piyasası kapsamındaki kabul edilen ve yerine getirilmiş yük atma teklifi miktarları toplamını (MWh),
 - TSM: vadeli elektrik piyasası, gün öncesi piyasası, gün içi piyasası satışları ile uzlaştırmaya esas ikili anlaşma satış miktarları ve dengeleme güç piyasası kapsamındaki kabul edilen ve yerine getirilmiş yük alma teklifi miktarları toplamını (MWh),
 - NAM: uzlaştırmaya esas veriş miktarı ile toplam alış ve satış miktarlarının kullanılması ile tespit edilen net alış miktarını (MWh),
 - NSM: uzlaştırmaya esas çekiş miktarı ile toplam alış ve satış miktarlarının kullanılması ile tespit edilen net satış miktarını (MWh),
 - PH : net alış miktarı ile net satış miktarı kullanılarak belirlenen piyasa hacmini (MWh),
 - DO : belirlenen dengesizlik oranını (%20),
 - Sinerji: dengeden sorumlu grup içerisinde sinerjiye dahil edilecek miktarı (MWh),
 - Cezalı Sinerji: dengeden sorumlu grup içerisinde sinerjiye dahil edilmeyen bireysel olacak değerlendirilen miktarı (MWh),
 - Negatif Cezalı Sinerji: dengeden sorumlu grup içerisinde sinerjiye dahil edilmeyen bireysel negatif cezalı tutarı (TL),
 - Pozitif Cezalı Sinerji: dengeden sorumlu grup içerisinde sinerjiye dahil edilmeyen bireysel pozitif cezalı tutarı (TL),
""")

    with st.expander("Özet Detaylar", expanded=True):
        st.dataframe(hesaplanan[['BEDM (MWh)', 'PH (MWh)', 'Hesaplanan DO (%)', 'Sinerji (MWh)',
            'Cezalı Sinerji (MWh)', 'Negatif Cezalı Sinerji (TL)',
            'Pozitif Cezalı Sinerji (TL)']].style.format(precision=2,thousands=".",decimal="."), use_container_width=True)
        
        st.write("""
 - BEDM: dengesizlik oranı tespitinde kullanılan bireysel enerji dengesizlik miktarını (MWh,
 - PH : net alış miktarı ile net satış miktarı kullanılarak belirlenen piyasa hacmini (MWh),
 - DO : belirlenen dengesizlik oranını (%20),
 - Sinerji: dengeden sorumlu grup içerisinde sinerjiye dahil edilecek miktarı (MWh),
 - Cezalı Sinerji: dengeden sorumlu grup içerisinde sinerjiye dahil edilmeyen bireysel olacak değerlendirilen miktarı (MWh),
 - Negatif Cezalı Sinerji: dengeden sorumlu grup içerisinde sinerjiye dahil edilmeyen bireysel negatif cezalı tutarı (TL),
 - Pozitif Cezalı Sinerji: dengeden sorumlu grup içerisinde sinerjiye dahil edilmeyen bireysel pozitif cezalı tutarı (TL),                 
""")
        



    res_cols = st.columns((1,1))
    with res_cols[0]:
        st.markdown("#### Taslak Dengesizlik Hesaplama Metodolojisine göre Hesaplama")

        
        total_sinerji = hesaplanan["Sinerji (MWh)"].sum() 
        total_sinerji_tl = total_sinerji*min(ptf,smf)*(1-dengesizlik_yuzde) if total_sinerji > 0 else max(ptf,smf)*(1+dengesizlik_yuzde)*total_sinerji
        total_negatif_cezalı_sinerji = hesaplanan["Negatif Cezalı Sinerji (TL)"].sum()
        total_pozitif_cezalı_sinerji = hesaplanan["Pozitif Cezalı Sinerji (TL)"].sum()
        total_cezalı_sinerji = total_negatif_cezalı_sinerji + total_pozitif_cezalı_sinerji

        st.write(f"""
 - İzin Verilen Toplam Sinerji (MWh): {total_sinerji:,.2f}
 - İzin Verilen Toplam Sinerji Tutarı (TL): {total_cezalı_sinerji:,.2f}
 - Toplam Negatif Cezalı Tutarı (TL): {total_negatif_cezalı_sinerji:,.2f}
 - Toplam Pozitif Cezalı Tutarı (TL): {total_pozitif_cezalı_sinerji:,.2f}
 - Toplam Tutar (TL): {total_sinerji_tl+total_cezalı_sinerji:,.2f}
""".replace(".","_").replace(",",".").replace("_",","))

    with res_cols[1]:
        st.markdown("#### Mevcut Dengesizlik Hesaplama Metodolojisine göre Hesaplama")
        önceki_sinerji = hesaplanan["BEDM (MWh)"].sum()
        önceki_total_sinerji_tl = önceki_sinerji*min(ptf,smf)*(1-dengesizlik_yuzde) if önceki_sinerji > 0 else max(ptf,smf)*(1+dengesizlik_yuzde)*önceki_sinerji

        st.write(f"""
 - Toplam Sinerji (MWh): {önceki_sinerji:,.2f}
 - Toplam Tutar (TL): {önceki_total_sinerji_tl:,.2f}""".replace(".","_").replace(",",".").replace("_",","))

else:
    st.write("Dosya yüklenmedi.")


## Footer
st.markdown("## ")
st.markdown("## ")
HtmlFile = open("./footer.html", 'r', encoding='utf-8')
footer = HtmlFile.read() 
components.html(footer, height = 400)
