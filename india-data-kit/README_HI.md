# India Data Kit – मुफ़्त NSE और BSE एंड-ऑफ़-डे डेटा पर अपने टूल बनाइए (Python · Excel · AI)

यह मुफ़्त, ओपन-सोर्स (MIT) किट **[WealthTechnical NSE/BSE EOD Downloader](https://www.wealthtechnical.com/eod-downloader/)** के डेटा फ़ोल्डर के साथ काम करती है। Downloader आपके PC पर स्प्लिट और बोनस के हिसाब से एडजस्ट किया हुआ NSE और BSE डेटा रखता है; यह किट उस डेटा पर स्कैनर, मार्केट ब्रेड्थ, सेक्टर रोटेशन, रिसर्च और दूसरे प्लेटफ़ॉर्म के लिए एक्सपोर्ट बनाने में मदद करती है।

> Downloader मुफ़्त है, पर उसका सोर्स कोड प्रकाशित नहीं किया गया है। यह किट सिर्फ़ **आपके PC** पर रखी फ़ाइलें पढ़ती है – इसमें कोई मार्केट डेटा नहीं है और यह कोई डेटा कहीं नहीं भेजती।

## क्या मिलेगा
* **एक लाइन में डेटा:** NSE/BSE शेयर, लगभग 100 NSE इंडेक्स (NIFTY50, NIFTYBANK, INDIAVIX…) और सभी वॉचलिस्ट (Nifty 50/100/200/500, Midcap, Smallcap, सेक्टर)
* **मार्केट ब्रेड्थ:** बढ़ने/गिरने वाले शेयर, A/D लाइन, 50 और 200 दिन के एवरेज से ऊपर शेयरों का %, नए 52-हफ़्ते के हाई/लो
* **सेक्टर रोटेशन:** हर NSE सेक्टर का 1 हफ़्ता / 1, 3, 6 महीने / 1 साल का रिटर्न
* **स्कैनर का उदाहरण:** 200-DMA से ऊपर, 52-हफ़्ते के हाई के पास, वॉल्यूम में उछाल – नियम आप बदल सकते हैं
* **एक्सपोर्ट:** एक CSV / Parquet / SQLite फ़ाइल, या **AmiBroker**, **NinjaTrader 8**, **MetaStock ASCII**, **MetaTrader 5** और बैकटेस्टिंग टूल्स के लिए हर शेयर की अलग CSV फ़ाइल
* **Downloader की अपनी जाँच:** क्वालिटी नोट्स, NSE बनाम BSE तुलना (ISIN से), लागू किए गए स्प्लिट/बोनस
* **हर शाम अपने-आप:** Downloader के अपडेट के बाद आपकी स्क्रिप्ट चलाइए ([गाइड](docs/AUTOMATION.md))
* **काल्पनिक सैंपल डेटा:** 40 काल्पनिक शेयर – असली मार्केट डेटा नहीं

## इंस्टॉल
```bash
pip install "https://github.com/wealthtechnical-afk/nse-bse-eod-downloader/archive/refs/heads/main.zip#subdirectory=india-data-kit"
```

## शुरुआत
```bash
pip install pandas matplotlib
cd india-data-kit/examples
python 01_quick_look.py            # काल्पनिक सैंपल डेटा
python 02_market_breadth.py auto   # आपका Downloader डेटा
python 03_sector_rotation.py auto
python 04_scanner.py auto
```

## ⚠ ज़रूरी सूचना
**यह मुफ़्त किट केवल शिक्षा और विश्लेषण के लिए है।** यह निवेश सलाह या किसी शेयर को ख़रीदने/बेचने की सिफ़ारिश नहीं है। WealthTechnical LLP SEBI-पंजीकृत निवेश सलाहकार या रिसर्च एनालिस्ट नहीं है, और NSE या BSE से संबद्ध नहीं है। फ़्यूचर्स और ऑप्शंस, क्रिप्टो और दूसरे सट्टा उपकरणों में ट्रेडिंग में नुक़सान का बड़ा जोखिम है; यह सिर्फ़ उन्हीं के लिए है जो इस जोखिम को समझते हैं और उठा सकते हैं। पूरा डिस्क्लेमर: https://www.wealthtechnical.com/disclaimer.html
