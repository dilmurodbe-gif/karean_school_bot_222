from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

router = Router()


# ================= GRAMMATIKA TUGMASI =================

@router.message(F.text == "📘 Grammatikalar")
async def grammar_books(message: Message):

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1A", callback_data="book_1A"),
                InlineKeyboardButton(text="1B", callback_data="book_1B")
            ],
            [
                InlineKeyboardButton(text="2A", callback_data="book_2A"),
                InlineKeyboardButton(text="2B", callback_data="book_2B")
            ],
            [
                InlineKeyboardButton(text="3A", callback_data="book_3A"),
                InlineKeyboardButton(text="3B", callback_data="book_3B")
            ],
            [
                InlineKeyboardButton(text="4A", callback_data="book_4A"),
                InlineKeyboardButton(text="4B", callback_data="book_4B")
            ],
            [
                InlineKeyboardButton(text="5A", callback_data="book_5A"),
                InlineKeyboardButton(text="5B", callback_data="book_5B")
            ],
            [
                InlineKeyboardButton(text="6A", callback_data="book_6A"),
                InlineKeyboardButton(text="6B", callback_data="book_6B")
            ]
        ]
    )

    await message.answer(
        "📚 Kerakli kitobni tanlang:",
        reply_markup=markup
    )


# ============== Grammar ================

grammar_1A = {
    "1A_1": "N+은/는::Urg'u va yuklama vafifasini bajaradi...",
    "1A_2": "N+입니까? / N+입니다::So‘roq va darak gap tuzishda ishlatiladi.\nMasalan: 학생입니까?\nO'quvchimi?\n네, 학생입니다.\nHa o'quvchidir.",
    "1A_3": "N+이/가 아닙니다::Inkor shaklida ishlatiladi\n'이 아닙니다' Undosh bilan tugasa\n '가 아닙니다'Unli bilan tugasa\n Masalan:저는 학생이 아닙니다.\n Men o'quvchi emasman.",
    "1A_4": "N+이/가 있어요 / 없어요::Bor / yo‘qni bildiradi.\nMasalan: 책이 있어요.\nKitob bor.\n컴퓨터가 없어요.\nKompyuter yo'q.",
    "1A_5": "이것은 / 그것은 / 저것은::Bu / u / anavi narsani bildiradi. Masalan: 이것은 책입니다.\nBu narsa kitob dir.",
    "1A_6": "주세요 ::Biror narsani iltimos qilish. Masalan: 물 좀 주세요.\nBiroz suv bering.",
    "1A_7": "N+하고 / 과/와 / (이)랑::\"...bilan\" ma'nosini beradi. Masalan: 친구하고 같이 갔어요.\nDo'stim bilan birga bordik.",
    "1A_8": "A/V + 아요 / 어요 / 해요::Fe’l yoki sifatga qo‘shilib, hozirgi yoki hozirgi zamonga yaqin ish-harakatni bildiradi.\n\n✅ Qoidalar:\n1) ㅏ/ㅗ bilan tugasa → 아요: 가다 → 가요 (boraman)\n2) boshqa unlilar bilan → 어요: 먹다 → 먹어요 (yeyman)\n3) 하다 bilan → 해요: 공부하다 → 공부해요 (dars qilaman)\n\n📌 Misollar:\n- 가요 (boraman)\n- 와요 (kelaman)\n- 먹어요 (yeyman)\n- 공부해요 (dars qilaman)",
    "1A_9": "N+을/를::-ni qo'shimchasi\nMasalan: 밥을 먹어요.\nOvqatNI yeyapman.",
    "1A_10": "N+에서::Harakat yoki holat sodir bo‘ladigan joylarga ishlatiladi. Masalan: 집에서 공부해요.\nUyda o'qiyapman.",
    "1A_11": "안 A/V::tarjimasi:-mayman\n-maydi\nInkor shakli. Masalan: 안 가요,\nBormayman\n안 먹어요.\nYemayman.",
    "1A_12": "N+에 있어요 / 없어요::Joy nomlariga nisbatan\nTarjimasi:-da bor\n-da yo'q\nMasalan: 교실에 책이 있어요.\nSinfxonada kitob bor.",
    "1A_13": "N+에 가요 / 와요::Yo‘nalish bildiradi.\nTarjimasi:-ga bormoq\n-dan kelmoq\nMasalan: 학교에 가요.\nMaktabga borayapman.",
    "1A_14": "앞 / 옆 / 뒤::Joylashuvlarga nisbatan ishlatiladi.\nTarjimasi:oldi, yon, orqa. Masalan: 집 앞에 있어요.\nUy yonida bor.",
    "1A_15": "요일::Haftaning kunlari: 월요일 (Dushanba),\n화요일 (Seshanba),\n수요일 (Chorshanba),\n목요일 (Payshanba),\n금요일 (Juma)\n토요일 (Shanba)\n일요일 (Yakshanba)",
    "1A_16": "N+에::Vaqt yoki joy bildiradi.\nTarjimasi:-da yoki -ga\nMasalan: 오전 9시에 학교에 가요.\nErtalab 9soatda maktabga boraman.",
    "1A_17": "A/V + 았/었/했어요::O‘tgan zamon.\n\n✅ Qoidalar:\n1) Fe’lning oxirgi bo‘g‘inida ㅏ yoki ㅗ bo‘lsa → 았어요: 가다 → 갔어요 (bordim)\n2) Boshqa unlilar bo‘lsa → 었어요: 먹다 → 먹었어요 (yedim)\n3) 하다 fe’li → 했어요: 공부하다 → 공부했어요 (o‘qidim)\n\n📌 Misollar:\n- 갔어요 (bordim)\n- 왔어요 (keldim)\n- 먹었어요 (yedim)\n- 공부했어요 (o‘qidim)",
    "1A_18": "A/V + 지만::Qarama-qarshi fikr.\nTarjimasi:ammo yoki lekin\nMasalan: 맛있지만 비싸요,\nMazzali lekin qimmat.",
    "1A_19": "V + 고::Ikki harakatlarni bir-biriga bog‘laydi.\nTarjimasi:-b yoki -ib \nMasalan: 밥을 먹고 공부해요,\nOvqatni yeb tahsil olyapman.",
    "1A_20": "V + (으)세요::Hurmat shakli.\nTarjimasi:-ing\nMasalan: 들어오세요,\nKiring.",
    "1A_21": "A/V + ㅂ/습니까?, ㅂ/습니다::Rasmiy so‘zlashuv uslubi. Masalan: 갑니까?\nBorasizmi,\n갑니다,\nBoraman.",
    "1A_22": "V + 을/ㄹ까요?::Taklif yoki mulohaza.\nTarjimasi:-mizmi\nMasalan: 갈까요?\nboramizmi.",
    "1A_23": "이/그/저::Ko‘rsatish olmoshlari: bu, u, anavi. Masalan: 이 사람,\nBu odam.",
    "1A_24": "A/V + 네요::Tarjimasi: ekan\nHayronlanish, ajablanish bildiradi. Masalan: 날씨가 좋네요!. Havo yaxshi ekan!"
}
grammar_1B = {
    "1B_1": "N+(의)::-ning ma'nosini beradi.\nMisol: 친구의 책 — do'stning kitobi",
    "1B_2": "N+을/를::-ni qo‘shimchasi (obyekt).\nMisol: 밥을 먹어요 — Ovqatni yeyapman",
    "1B_3": "N+(이)세요::Hurmat shakli '...lar'.\nMisol: 선생님이세요 — Ustozlar",
    "1B_4": "V+(으)시::Hurmat ifodasi.\nMisol: 가시다 — Boradilar (hurmat bilan)",
    "1B_5": "N+부터, 까지::'dan ... gacha'.\nMisol: 아침부터 저녁까지 — Ertalabdan kechgacha",
    "1B_6": "V+아서/어서::-ib, bo‘lib.\nMisol: 공부해서 피곤해요 — O'qib charchadim",
    "1B_7": "V+(으)ㄹ 거예요::Kelasi zamon.\nMisol: 갈 거예요 — Boraman",
    "1B_8": "V+지 마세요::...mang (taqiqlov).\nMisol: 가지 마세요 — Bormang",
    "1B_9": "N+만::Faqat.\nMisol: 물만 마셔요 — Faqat suv ichaman",
    "1B_10": "V+아/어야 되다::...qilish kerak.\nMisol: 공부해야 돼요 — Dars qilish kerak",
    "1B_11": "V+아요/어요/지요?::So‘roq shakli.\nMisol: 맛있지요? — Mazalimi?",
    "1B_12": "V+고 있다::Hozirgi davomiy holat.\nMisol: 먹고 있어요 — Yeyayapman",
    "1B_13": "V+못::Qila olmaslik.\nMisol: 못 가요 — Bormayman (eplay olmayman)",
    "1B_14": "A/V+아서/어서::...ligi uchun.\nMisol: 예뻐서 좋아요 — Chiroyli bo‘lgani uchun yoqadi",
    "1B_15": "V+(으)려고 하다::...moqchi bo‘lmoq.\nMisol: 가려고 해요 — Borishni niyat qilayapman",
    "1B_16": "V+아/어 주다::...ib bering.\nMisol: 도와주세요 — Yordam bering",
    "1B_17": "(으)N+로::...ga, orqali.\nMisol: 버스로 가요 — Avtobus bilan boraman",
    "1B_18": "(으)N+L::Ot yasovchi qo‘shimcha.\nMisol: 공부한 사람 — O‘qigan odam",
    "1B_19": "N+한테 / 께::Shaxsga (hurmatli).\nMisol: 선생님께 드려요 — Ustozga beraman",
    "1B_20": "V+아/어 보세요::...ib ko‘ring.\nMisol: 입어 보세요 — Kiyib ko‘ring",
    "1B_21": "A/V+(으)면::...sa, agar.\nMisol: 비가 오면 안 가요 — Yomg‘ir yog‘sa bormayman",
    "1B_22": "V+는::Ot yasovchi zamon qo‘shimchasi.\nMisol: 먹는 사람 — Yeyayotgan odam",
    "1B_23": "V+고 싶다 (1-shaxs)::...moqchiman.\nMisol: 한국에 가고 싶어요 — Koreyaga bormoqchiman",
    "1B_24": "V+고 싶어 하다 (3-shaxs)::...moqchi (u).\nMisol: 동생이 먹고 싶어 해요 — Ukam yegisi kelayapti",
    "1B_25": "V+(으)ㄹ 수 있다 / 없다::Qila olish / qilolmaslik.\nMisol: 수영할 수 있어요 — Suzishni bilaman",
    "1B_26": "V+(으)러 가다 / 오다::...gani bormoq / kelmoq.\nMisol: 공부하러 가요 — O‘qigani boraman",
    "1B_27": "V+(으)면서::...ib, bir vaqtda.\nMisol: 음악을 들으면서 공부해요 — Musiqa eshitib dars qilaman"
}
grammar_2A = {
    "2A_1": "N+(이)라고 하다::학생이라고 해요. (haksaeng-irago haeyo) – U o‘zini o‘quvchi deb aytadi.",
    "2A_2": "V+(으)려고::공부하려고 해요. (gongbu-haryeogo haeyo) – Dars qilmoqchiman.",
    "2A_3": "A/V + 거나::책을 읽거나 음악을 들어요. – Kitob o‘qiyman yoki musiqa tinglayman.",
    "2A_4": "N+(이)나::물이나 주스를 마셨어요. – Suv yoki sharbat ichdim.",
    "2A_5": "V+는 것::운동하는 것을 좋아해요. – Sport bilan shug‘ullanishni yaxshi ko‘raman.",
    "2A_6": "V+을/ㄹ 줄 알다::수영할 줄 알아요. – Suza olaman.",
    "2A_7": "A/V+지 않다::먹지 않아요. – Yeymayapman.",
    "2A_8": "N+동안::1년 동안 한국에 있었어요. – 1 yil davomida Koreyada edim.",
    "2A_9": "A+은/ㄴ 데::비싼 데 좋아요. – Qimmat, lekin yaxshi.",
    "2A_10": "V+을/ㄹ::읽을 책이에요. – O‘qiladigan kitob.",
    "2A_11": "A+(으)ㄴ 것 같다::예쁜 것 같아요. – Chiroyli ko‘rinadi.",
    "2A_12": "N+보다::사과보다 배가 더 맛있어요. – Olmadan ko‘ra nok mazaliroq.",
    "2A_13": "V+았/었/했으면 좋겠다::한국에 갔으면 좋겠어요. – Koreyaga borganimni xohlardim.",
    "2A_14": "A/V+을/ㄹ 까요?::같이 갈까요? – Birga boramizmi?",
    "2A_15": "A/V+을/ㄹ 거예요::내일 만날 거예요. – Ertaga uchrashamiz.",
    "2A_16": "A/V+(으)니까::늦었으니까 빨리 가요. – Kechikdik, shuning uchun tezroq ketaylik.",
    "2A_17": "V+고 나서::밥을 먹고 나서 공부했어요. – Ovqat yegach dars qildim.",
    "2A_18": "N+(으)로::버스로 갔어요. – Avtobusda bordim.",
    "2A_19": "N+(이)라서::학생이라서 돈이 없어요. – O‘quvchi bo‘lganim uchun pulim yo‘q.",
    "2A_20": "V+(으)면 되다::버튼을 누르면 돼요. – Tugmani bossangiz bo‘ladi.",
    "2A_21": "V+(으)ㄴ 것 같다::간 것 같아요. – Ketgandek tuyuladi.",
    "2A_22": "A/V+(으)ㄹ 것 같다::비가 올 것 같아요. – Yomg‘ir yog‘adiganga o‘xshaydi.",
    "2A_23": "V+는지 알다::그 사람이 어디 사는지 알아요? – U odam qayerda yashashini bilasizmi?",
    "2A_24": "N+인지 알다::그 사람이 의사인지 알아요. – U odam shifokorligini bilaman.",
    "2A_25": "V+(으)려면::한국어를 잘하려면 많이 연습해야 해요. – Koreys tilini yaxshi bilmoqchi bo‘lsangiz, ko‘p mashq qilishingiz kerak.",
    "2A_26": "V+다가::텔레비전을 보다가 잤어요. – Televizor ko‘rayotib uxlab qolganman.",
    "2A_27": "A/V+겠::맛있겠어요. – Mazali bo‘lsa kerak.",
    "2A_28": "V+아/어 버리다::잊어 버렸어요. – Unutib yubordim.",
    "2A_29": "N+때문에::감기 때문에 못 갔어요. – Shamollaganim uchun bora olmadim.",
    "2A_30": "A/V+(으)ㄹ 때::어릴 때 한국에 갔어요. – Yoshligimda Koreyaga borganman.",
    "2A_31": "A/V/N+데요::예쁜데요! – Chiroyli ekan-ku!",
    "2A_32": "V+는 중이다::공부하는 중이에요. – Dars qilayotgan paytdaman.",
    "2A_33": "N+중이다::회의 중입니다. – Hozir yig‘ilishdamiz.",
    "2A_34": "N+밖에::물밖에 없어요. – Faqat suv bor, boshqa narsa yo‘q."
}
grammar_2B = {
    "2B_1": "N+중에(서)::... ichida, orasida tanlashda ishlatiladi.::과일 중에서 딸기를 제일 좋아해요.::Mevalar ichida qulupnayni eng yaxshi ko‘raman.",
    "2B_2": "V+(으)ㄹ래요::...moqchimisiz? / niyatni bildiradi.::영화 볼래요?::Kino ko‘rmoqchimisiz?",
    "2B_3": "A+(으)ㄴ 데 , V+는데, N+인데::Ammo, lekin, shunday bo‘lsa-da degan ma’no beradi.::오늘은 바쁜데 내일은 괜찮아요.::Bugun bandman, lekin ertaga bo‘shman.",
    "2B_4": "V+는 게 어때요::...qilish qanday? (taklif berishda ishlatiladi)::산책하는 게 어때요?::Sayr qilish qanday fikr?",
    "2B_5": "V+기로 하다::Qaror bildirish – ...ishga qaror qilmoq.::매일 운동하기로 했어요.::Har kuni sport qilishga qaror qildim.",
    "2B_6": "A+아/어/해 보이다::Ko‘rinmoq (tashqi holat ifodasi).::기분이 좋아 보여요.::Kayfiyatingiz yaxshi ko‘rinadi.",
    "2B_7": "N+처럼/같이::...dek, ...kabidir.::그 사람은 연예인처럼 예뻐요.::U odam san’atkordek chiroyli.",
    "2B_8": "A+(으)ㄴ 편이다, V+는 편이다::Nisbatan shunday deyish mumkin.::저는 매운 음식을 잘 먹는 편이에요.::Men achchiq ovqatni yaxshi yeydigan odamman.",
    "2B_9": "A+게::Sifat ravishga aylanadi – qanday tarzda?::조용하게 말했어요.::Tinchgina gapirdi.",
    "2B_10": "A/V+(으)ㄹ 지 모르겠다::Ishonchsizlik, bilmaslik bildiradi.::비가 올지 모르겠어요.::Yomg‘ir yog‘adimi, bilmayman.",
    "2B_11": "A/V+기는 하지만::Garchi ... bo‘lsa ham.::좋기는 하지만 너무 비싸요.::Yaxshi, lekin juda qimmat.",
    "2B_12": "A/V+기 때문에, N+(이)기 때문에::Sabab bildirish – ...gani uchun.::피곤하기 때문에 못 갔어요.::Charchaganim uchun bora olmadim.",
    "2B_13": "V+기(가)::Fe’lni otlash – ...ish (harakat) sifatida.::한국어 공부하기가 어려워요.::Koreys tilini o‘rganish qiyin.",
    "2B_14": "V+(으)ㄴ 적(이) 있다/없다::Tajriba bildiradi – qilgan/ qilmagan.::한복을 입은 적이 있어요.::Hanbok kiyganman.",
    "2B_15": "A/V+았/었/했을 때::...gan vaqtda, paytda.::한국에 갔을 때 친구를 만났어요.::Koreyaga borganda do‘stimni uchratdim.",
    "2B_16": "V+아도/어도/해도 되다::Ruxsat berish – ...qilsa bo‘ladi.::질문해도 돼요?::Savol bersam bo‘ladimi?",
    "2B_17": "V+(으)면 안 되다::Taqiqlash – ...qilsa bo‘lmaydi.::여기에서 사진을 찍으면 안 돼요.::Bu yerda suratga olish mumkin emas.",
    "2B_18": "V+아지다/어지다::O‘zgarish – ...bo‘lib qolmoq.::날씨가 추워졌어요.::Havo sovib ketdi.",
    "2B_19": "V+게 되다::Holat o‘zgarishi – ...bo‘lib qoldi.::한국어를 잘하게 됐어요.::Koreys tilini yaxshi biladigan bo‘ldim.",
    "2B_20": "V+기 전에::...dan oldin.::자기 전에 이를 닦아요.::Uxlashdan oldin tishimni yuvaman.",
    "2B_21": "V+(으)ㄴ 후에::...dan keyin.::수업이 끝난 후에 밥을 먹었어요.::Dars tugagandan keyin ovqatlandim.",
    "2B_22": "V+아/어/해 놓다::...qilib qo‘ymoq, tayyor holda qoldirmoq.::문을 열어 놓았어요.::Eshikni ochiq qoldirdim.",
    "2B_23": "N+대신::...o‘rniga.::커피 대신 물을 마셨어요.::Qahva o‘rniga suv ichdim.",
    "2B_24": "V+(으)ㄹ까 하다::...qilmoqchidekman (reja, niyat).::오늘은 집에 있을까 해요.::Bugun uyda qolmoqchiman deb o‘ylayapman.",
    "2B_25": "A/V+(으)ㄹ 테니까::...bo‘ladi, shuning uchun.::제가 도와줄 테니까 걱정하지 마세요.::Men yordam beraman, shuning uchun havotir olmang.",
    "2B_26": "V+아다/어다 주다::... qilib berish.::물을 가져다 주세요.::Suv olib bering, iltimos.",
    "2B_27": "V+(으)ㄹ 뻔하다::Sal qolib... bo‘lishi.::넘어질 뻔했어요.::Yiqilib tushayozdim.",
    "2B_28": "V+아/어 있다::Holat davom etmoqda.::불이 켜져 있어요.::Chiroq yoqilgan holatda turibdi.",
    "2B_29": "(으)ㄴ 지 (시간) 되다/지나다::Qancha vaqt o‘tganini bildirish.::운동을 시작한 지 두 달 됐어요.::Sportni boshlaganimga ikki oy bo‘ldi.",
    "2B_30": "N+(이)나::Yoki / hatto / ...kabi variantlardan foydalaniladi.::친구나 가족과 여행을 가고 싶어요.::Do‘stim yoki oilam bilan sayohatga bormoqchiman.",
    "2B_31": "A+다, V+ㄴ/는다, N+(이)다::Xolis, rasmiy, fakt shaklidagi gap (yozma uslub).::이 옷은 예쁘다.::Bu kiyim chiroyli."
}

grammar_3A = {
    "3A_1": "A+다고 하다, V+ㄴ/는다고 하다, N+(이)라고 하다::Boshqaning gapini yetkazish (間接話法).::민수가 내일 온다고 했어요.::Minsoo ertaga kelishini aytdi.",
    "3A_2": "V+아야/어야겠다::Qaror yoki majburiyatni bildirish.::이제 집에 가야겠어요.::Endi uyga borishim kerak.",
    "3A_3": "A+다고 들었다, V+ㄴ/는다고 들었다, N+(이)라고 들었다::Eshitilgan gapni yetkazish.::그 영화가 재미있다고 들었어요.::U film qiziqarli ekan deb eshitdim.",
    "3A_4": "A+대요, V+ㄴ/는대요, N+(이)래요::Qisqa間接話法 – boshqalarning so‘zini qisqartirib aytish.::친구가 내일 이사한대요.::Do‘stim ertaga ko‘charmish.",
    "3A_5": "V+자마자::...bilanoq, darhol.::집에 오자마자 샤워했어요.::Uyga kelishim bilan dush qildim.",
    "3A_6": "V+(으)라고 하다::Buyruq yoki iltimosni uzatish.::선생님이 조용하라고 했어요.::O‘qituvchi jim bo‘lishni aytdi.",
    "3A_7": "V+느라고::Bir ish tufayli boshqa ishni qilolmaslik.::공부하느라고 전화를 못 받았어요.::O‘qiyotganim uchun telefonga javob berolmadim.",
    "3A_8": "누구나, 언제나, 어디나, 무엇이나::Har kim, har qachon, har joyda, har qanday narsa.::누구나 실수할 수 있어요.::Har kim xato qilishi mumkin.",
    "3A_9": "N+(이)나::Kutilganidan ko‘p yoki ta’kid.::커피를 네 잔이나 마셨어요.::To‘rt piyola qahva ichdim!",
    "3A_10": "A/V+을/ㄹ 텐데::Taxmin + izoh yoki afsus.::눈이 올 텐데 나가지 마세요.::Yomg‘ir yog‘sa kerak, chiqmang.",
    "3A_11": "A+(으)냐고 하다, V+느냐고 하다, N+(이)냐고 하다::Savol shaklini uzatish (間接).::친구가 언제 오느냐고 했어요.::Do‘stim qachon kelasan deb so‘radi.",
    "3A_12": "A/V+(으)ㄹ 줄 몰랐다::Kutilmagan holat.::그 사람이 그렇게 빨를 줄 몰랐어요.::U odam shunchalik tezligini bilmasdim.",
    "3A_13": "V+자고 하다::Taklifni uzatish.::친구가 같이 가자고 했어요.::Do‘stim birga boraylik dedi.",
    "3A_14": "A+(으)ㄴ가 보다, V+나 보다, N+인가 보다::Taxmin ifodasi.::비가 오는가 봐요.::Yomg‘ir yog‘ayotganga o‘xshaydi.",
    "3A_15": "V+아/어 보니까::Qilganidan keyingi tushuncha.::먹어 보니까 정말 맛있어요.::Yeb ko‘rsam, juda mazali ekan.",
    "3A_16": "A/V+던데(요)::Ko‘rgan, boshidan kechirgan tajriba.::그 영화 재미있던데요.::U film qiziqarli ekan (ko‘rdim).",
    "3A_17": "V+(으)ㄹ까 말까 (하다)::Ikkilanmoq.::갈까 말까 해요.::Bormay qo‘yaymi yo boraymi deb turibman.",
    "3A_18": "V+지 그래요?::Taklif qilish.::좀 쉬지 그래요?::Biroz dam olsangizchi?",
    "3A_19": "V+(으)ㄹ 걸 그랬다::Afsus ifodasi.::일찍 올 걸 그랬어요.::Erta kelishim kerak edi (afsus).",
    "3A_20": "A/V+거든(요), N+(이)거든(요)::Sabab bildiradi.::피곤하거든요.::Charchaganim uchun.",
    "3A_21": "V+이/히/리/기 (피동)::Majhul nisbat.::문이 열렸어요.::Eshik ochildi.",
    "3A_22": "V+았다가/었다가::Harakatdan so‘ng qarama-qarshi holat.::나갔다가 다시 들어왔어요.::Chiqib, yana kirdim.",
    "3A_23": "A+(으)ㄴ 데도, V+는 데도, N+인데도::...bo‘lishiga qaramay.::추운데도 나갔어요.::Sovuq bo‘lishiga qaramay, chiqdim.",
    "3A_24": "A/V+더니::Oldingi tajriba + keyingi natija.::그 사람 열심히 공부하더니 1등 했어요.::U odam ko‘p o‘qidi, 1-chi bo‘ldi.",
    "3A_25": "V+도록 하다::Buyruq yoki maslahat.::조용히 하도록 하세요.::Tinch bo‘ling.",
    "3A_26": "V+다(가)::Harakat o‘rtasida boshqa holat.::공부하다가 잤어요.::Dars qilayotib uxlab qoldim.",
    "3A_27": "A+다고(요), V+ㄴ/는다 고(요), N+(이)라고(요)?::So‘zni qaytarish, ajablanish.::뭐라고요? 다시 말해 주세요.::Nima dedingiz? Qayta ayting iltimos.",
    "3A_28": "아무리 A/V+아도/어도::Qanchalik ... qilsa ham.::아무리 바빠도 운동해요.::Qanchalik band bo‘lsam ham sport qilaman.",
    "3A_29": "A/V+아야/어야 할 텐데::Xavotir yoki istak.::비가 안 와야 할 텐데.::Yomg‘ir yog‘masa yaxshi bo‘lardi.",
    "3A_30": "N+을/를 위해(서), V+기 위해서::...uchun, maqsad ifodasi.::건강을 위해서 운동해요.::Salomatlik uchun sport qilaman.",
    "3A_31": "V+아지다/어지다::O‘zgarish, passiv shakl.::문이 닫아졌어요.::Eshik yopildi.",
    "3A_32": "A+(으)ㄴ 데도 불구하고, V+는데도 불구하고, N+인데도 불구하고::...ga qaramay.::비가 오는데도 불구하고 갔어요.::Yomg‘ir yog‘ayotganiga qaramay bordim.",
    "3A_33": "N+에 대해(서), N+에 대한::...haqida.::한국 문화에 대해 배워요.::Koreys madaniyati haqida o‘rganaman."
}

grammar_3B = {
    "3B_1": "A/V+던::O‘tgan, lekin hali tugamagan yoki davomiy ish-harakatlar.::자주 가던 식당이에요.::Tez-tez boradigan restoran edi.",
    "3B_2": "A/V+잖아(요)::Axir...,-ku! (Eslatish, e’tiroz bildiradi).::늦었잖아요!::Axir kech qolding-ku!",
    "3B_3": "V+(으)ㄹ 생각/계획/예정이다::Reja, niyatni bildiradi.::주말에 여행 갈 계획이에요.::Hafta oxiri sayohatga borish rejam bor.",
    "3B_4": "V+(으)려면 멀었다::Hali uzoq, hali vaqt kerak.::졸업하려면 멀었어요.::Bitirguncha hali uzoq.",
    "3B_5": "V+이/히/리/기/우 (사동)::Majbur qilish (causative).::아이를 재웠어요.::Bolani uxlatdim.",
    "3B_6": "A+다면, V+ㄴ/는다면, N+이라면::Agar... bo‘lsa (faraz).::시간이 있다면 만나요.::Agar vaqtingiz bo‘lsa, uchrashaylik.",
    "3B_7": "A+(으)ㄴ 모양이다, V+는 모양이다, N+인 모양이다::...ga o‘xshaydi (tahmin).::밖에 비가 오는 모양이에요.::Tashqarida yomg‘ir yog‘ayotganga o‘xshaydi.",
    "3B_8": "A/V+아야/어야, N+이어야/여야::...kerak, shart.::열심히 공부해야 성공해요.::Yaxshi o‘qish kerak, shunda muvaffaqiyat bo‘ladi.",
    "3B_9": "A/V+(으)ㄹ까 봐::...deb xavotirlanib.::늦을까 봐 뛰어왔어요.::Kech qolaman deb yugurib keldim.",
    "3B_10": "V+고 있다::Harakatning davomiy holati.::친구를 기다리고 있어요.::Do‘stimni kutyapman.",
    "3B_11": "A/V+도록::...gacha, ...uchun (maqsad, daraja).::공부를 열심히 하도록 하세요.::Yaxshi o‘qish uchun harakat qiling.",
    "3B_12": "하도 A/V+아서/어서::Juda...ligi sababli.::하도 피곤해서 일찍 잤어요.::Juda charchaganim uchun erta yotdim.",
    "3B_13": "A/V+았던/었던::O‘tmishda bo‘lgan, endi tugagan holat.::전에 먹었던 음식이에요.::Oldin yegan ovqatim bu.",
    "3B_14": "A+아/어 하다::Boshqaning hissiyotini ifodalash.::아이들이 무서워해요.::Bolalar qo‘rqyapti.",
    "3B_15": "A/V+(으)면 A/V+(으)ㄹ수록::Qanchalik... shunchalik...::공부하면 할수록 재미있어요.::Qanchalik o‘qisangiz, shunchalik qiziqarli bo‘ladi.",
    "3B_16": "V+게 하다::...qilishga majburlamoq (yordami bilan qilish).::엄마가 아이를 울게 했어요.::Ona bolani yig‘latdi.",
    "3B_17": "A/V+(으)ㄹ 걸(요)::Taxmin, afsus yoki istak bildiradi.::비가 올 걸요.::Yomg‘ir yog‘sa kerak.",
    "3B_18": "A/V+지 않으면 안 되다::...qilmaslik mumkin emas (majburiy).::약을 먹지 않으면 안 돼요.::Dori ichmasangiz bo‘lmaydi.",
    "3B_19": "V+는 길에::Yo‘l-yo‘lakay, ...ketayotib.::학교 가는 길에 친구를 만났어요.::Maktabga ketayotib do‘stimni uchratdim.",
    "3B_20": "N+만 하다::...dek, ...kabi bo‘lmoq.::그 아이는 토끼만 해요.::U bola quyondek kichkina.",
    "3B_21": "V+(으)ㄹ 생각도 못 하다::Hech o‘ylab ham ko‘rmagan, kutilmagan.::이렇게 될 줄은 생각도 못 했어요.::Bunday bo‘ladi deb o‘ylamagan edim.",
    "3B_22": "V+(으)ㄹ 만 하다::Qilishga arziydi.::이 영화는 볼 만 해요.::Bu filmni ko‘rishga arziydi.",
    "3B_23": "A/V+기로 유명하다, N+으로 유명하다::... bilan mashhur.::부산은 해운대로 유명해요.::Pusan Haeundae sohili bilan mashhur.",
    "3B_24": "V+고 보니::Qilganimdan keyin anglash.::가고 보니 문이 닫혔어요.::Borgandim, eshik yopilgan ekan.",
    "3B_25": "A+(으)ㄴ 척하다, V+는 척하다, N+인 척하다::Go‘yoki... qilmoq (soxta harakat).::모르는 척했어요.::Bilmaganday qildim.",
    "3B_26": "A/V+다니요, N+(이)라니요::Hayrat, tasdiq yoki e’tiroz.::그 사람이 학생이라니요?::U odam talaba emishmi?",
    "3B_27": "N+(이)라고 해서, A+ㄴ 것은 아니다, V+는 것은 아니다::Doim ham emas.::공부를 많이 한다고 해서 성적이 좋은 건 아니에요.::Ko‘p o‘qigan har doim ham yaxshi baho oladi degani emas.",
    "3B_28": "A+다니까요, V+ㄴ/는다니까요, N+(이)라니까요::Ta’kid, ishonch, e’tiroz.::맞다니까요!::To‘g‘ri deyapman-ku!",
    "3B_29": "V+고 말다::Oxirida ... bo‘lib qoldi (afsus/majburlik).::늦잠을 자고 말았어요.::Oxiri uxlab qolibman."
}

grammar_4A = {
    "4A_1": "A+다면서요, V+ㄴ/는 다면서요, N+(이)라면서요::Eshitgan narsani tasdiqlab so‘rash (axborotni tekshirish).::한국에 간다면서요?::Eshitishimcha Koreyaga ketayapsizmi?",
    "4A_2": "V+다보면::...qilaversang, ...bo‘ladi.::공부하다보면 실력이 늘어요.::O‘qiyversang, bilim oshadi.",
    "4A_3": "N+은/는, A+다는 것이다/점이다, V+ㄴ/는다는 것이다/점이다::Asosiy fikrni ta’kidlash.::중요한 점은 건강하다는 것입니다.::Muhim jihati sog‘lom ekanligidir.",
    "4A_4": "V+는 대로, N+대로::Darhol, ...ga binoan.::도착하는 대로 전화할게요.::Yetib borishim bilanoq qo‘ng‘iroq qilaman.",
    "4A_5": "어찌나(얼마나) A+(으)ㄴ지, V+는지::Qanchalik ...ligi sababli (hayrat, kuchli ifoda).::어찌나 피곤한지 바로 잠들었어요.::Shunchalik charchadimki, darrov uxlab qoldim.",
    "4A_6": "A/V+(으)ㄹ 정도로, N+정도이다::Darajada, shu qadar.::다리가 아플 정도로 많이 걸었어요.::Oyoqlarim og‘rigan darajada yurdim.",
    "4A_7": "V+다가는::Agar doimiy ravishda ..., yomon oqibat.::그렇게 먹다가는 병에 걸려요.::Shunday ovqatlanaversang, kasal bo‘lasan.",
    "4A_8": "A/V+(으)ㄹ 뿐만 아니라, N+뿐만 아니라::Na faqat ..., balki.::그 사람은 예쁠 뿐만 아니라 똑똑해요.::U odam nafaqat chiroyli, balki aqlli ham.",
    "4A_9": "V+(으)나마나::Hech foydasi yo‘q (qilsa ham, qilmasa ham baribir).::말해봤자 듣지 않을 거예요.::Gapirsam ham, baribir eshitmaydi.",
    "4A_10": "V+는 바람에::Kutilmagan sabab tufayli.::늦잠을 자는 바람에 지각했어요.::Uzoq uxlaganim sababli kechikdim.",
    "4A_11": "N+(이)라는::...nomli, deb ataluvchi.::한국이라는 나라::'Koreya' deb ataluvchi mamlakat.",
    "4A_12": "N+제시해(서)::...ni ko‘rsatib, taklif qilib.::자료를 제시해서 설명했어요.::Materialni ko‘rsatib tushuntirdim.",
    "4A_13": "A/V+기는커녕, N+은/는커녕::... u yoqda tursin, aksincha.::운동은커녕 산책도 안 해요.::Sport u yoqda tursin, sayr ham qilmaydi.",
    "4A_14": "A+(으)ㄴ 반면(에), V+는 반면(에)::...ga nisbatan, ... bo‘lsa-da.::그 식당은 맛있는 반면에 비싸요.::U restoran mazali, lekin qimmat.",
    "4A_15": "A/V+(으)ㄹ 수밖에 없다::Majbur, boshqa iloji yo‘q.::도와줄 수밖에 없어요.::Yordam berishdan boshqa ilojim yo‘q.",
    "4A_16": "A+다더니, V+ㄴ/는다더니::Eshitgan gap haqiqat ekanligini ko‘rsatadi.::그 사람이 잘한다더니 정말 잘하네요.::U odam yaxshi qiladi degandilar, rostdan ham yaxshi qiladi.",
    "4A_17": "A/V+기 마련이다::...bo‘lishi tabiiy, muqarrar.::사람은 누구나 실수하기 마련이에요.::Har kim xato qiladi – bu tabiiy.",
    "4A_18": "V+다보니까::...qila-qila (natijada).::공부하다 보니까 재미있어졌어요.::O‘qiyverganim sayin qiziqarli bo‘lib ketdi.",
    "4A_19": "A/V+기는(요)::E’tiroz bildiradi, rad etish.::무섭기는요. 전혀 안 무서워요.::Qo‘rqinchli emishmi! Umuman qo‘rqinchli emas.",
    "4A_20": "A/V+든(지), N+(이)든(지)::...bo‘lishidan qat’i nazar.::누구든지 환영합니다.::Kim bo‘lishidan qat’i nazar, xush kelibsiz.",
    "4A_21": "N+(이)야말로::Aynan ...ning o‘zi.::이것이야말로 진정한 사랑이에요.::Bu aynan chinakam muhabbat.",
    "4A_22": "여간 A+(으)ㄴ 것이 아니다, V+는 것이 아니다::Juda ... (inkor orqali kuchaytirish).::그 사람은 여간 똑똑한 게 아니에요.::U odam juda aqlli.",
    "4A_23": "A/V+더라도, 아도/어도::... bo‘lsa ham.::바빠도 운동은 해야 해요.::Band bo‘lsam ham sport qilaman.",
    "4A_24": "A+다고 보다, V+ㄴ/는다고 보다::...deb hisoblamoq, fikr bildirish.::저는 그게 맞다고 봐요.::Menimcha, bu to‘g‘ri.",
    "4A_25": "V+(으)ㄴ 채(로)::... holatda (qilib turib).::신발을 신은 채 방에 들어왔어요.::Poyabzal kiygan holda xonaga kirdi.",
    "4A_26": "A+(으)ㄴ지, V+는지::...mi yo‘qmi (bilish uchun).::그 사람이 학생인지 알아요?::U odam talaba ekanligini bilasizmi?",
    "4A_27": "V+아다(가)/어다(가)::Harakatni bajarib boshqa harakatni qilish.::물을 떠다가 꽃에 줬어요.::Suv olib, gulga quydim.",
    "4A_28": "A+다는, V+ㄴ/는다는::... degan (nisbat shakli).::친구가 간다는 식당이에요.::Do‘stim aytgan restoran bu.",
    "4A_29": "N+을/를 비롯해서(비롯한)::...ni o‘z ichiga olib, ...dan boshlab.::과일을 비롯해서 많은 음식을 샀어요.::Mevani o‘z ichiga olgan holda ko‘p ovqat oldim.",
    "4A_30": "A/V+거든::Agar ... bo‘lsa / sabablovchi gap.::시간 있거든 좀 도와주세요.::Agar vaqtingiz bo‘lsa, yordam bering.",
    "4A_31": "A/V+았더라면/었더라면::...qilganimda edi (afsus).::일찍 잤더라면 피곤하지 않았을 거예요.::Erta yotganimda edi, charchamas edim.",
    "4A_32": "A/V+(으)ㅁ::Fe’l yoki sifatni otlash (formal uslub).::공부함은 중요하다.::O‘qish muhimdir.",
    "4A_33": "A+(으)ㄴ 듯하다, V+는 듯하다::...dek ko‘rinadi (ehtimol).::비가 올 듯해요.::Yomg‘ir yog‘adiganga o‘xshaydi."
}

grammar_4B = {
    "4B_1": "V+(으)ㄹ 리(가) 없다::Imkoni yo‘q, bo‘lishi mumkin emas.::그럴 리가 없어요.::Bunday bo‘lishi mumkin emas.",
    "4B_2": "V+기(가) 무섭게 / (자마자)::... bilanoq, darhol.::문을 열자마자 전화가 왔어요.::Eshikni ochishim bilan telefon keldi.",
    "4B_3": "N+만에::...dan keyin (oradan o‘tgan vaqt).::삼 일만에 만났어요.::Uch kundan keyin uchrashdik.",
    "4B_4": "A/V+(으)나 / 그러나::Ammo, lekin, biroq.::좋기는 하나 너무 비싸요.::Yaxshi, lekin juda qimmat.",
    "4B_5": "A/V+더라고(요)::Shaxsan ko‘rgan, eshitgan tajriba.::그 영화 정말 재미있더라고요.::U film haqiqatan qiziqarli ekan.",
    "4B_6": "N+치고::...ning hammasi / istisnosiz.::학생치고 그 사실을 모르는 사람 없어요.::Talabalardan bu narsani bilmaydigan yo‘q.",
    "4B_7": "A+다는 것은, V+ㄴ/는다는 것은, N+(으)로 알 수 있다::... degani, ... orqali bilish mumkin.::그가 성실하다는 것은 출근 시간에서 알 수 있어요.::Uning halolligini ishga kelish vaqtidan bilsa bo‘ladi.",
    "4B_8": "N+에 의하면::...ga ko‘ra (manbaga tayangan holda).::뉴스에 의하면 내일 비가 온대요.::Yangiliklarga ko‘ra ertaga yomg‘ir yog‘adi ekan.",
    "4B_9": "A/V+(으)ㄹ지도 모르다 / V+(으)ㄹ 수 있다::Balki ..., ehtimol; mumkin.::길이 막힐지도 몰라요.::Yo‘l tirband bo‘lishi mumkin.",
    "4B_10": "A+(으)ㄴ가?, V+는가?, N+인가?::Savol shakli – rasmiy uslubda.::그것이 사실인가요?::Bu haqiqatmi?",
    "4B_11": "N+마저::Hatto ..., gacha.::그 사람마저 떠났어요.::Hatto u odam ham ketdi.",
    "4B_12": "V+는 김에::Shu bahona bilan, imkoniyatdan foydalanib.::밖에 나가는 김에 쓰레기를 버렸어요.::Tashqariga chiqayotganim bahona chiqindini tashladim.",
    "4B_13": "N+(이)면::Agar ... bo‘lsa.::학생이면 할인이 있어요.::Agar talaba bo‘lsangiz, chegirma bor.",
    "4B_14": "V+느니 차라리::... qilgandan ko‘ra, yaxshisi...::기다리느니 차라리 집에 갈게요.::Kutadurgandan ko‘ra uyga ketaman.",
    "4B_15": "N+에 따라(서)::...ga qarab, muvofiq.::날씨에 따라서 옷을 입어요.::Ob-havoga qarab kiyim kiyaman.",
    "4B_16": "A+(으)ㄴ 데다가, V+는 데다가::...ga qo‘shimcha ravishda.::그 식당은 맛있는 데다가 싸요.::U restoran mazali, ustiga-ustak arzon.",
    "4B_17": "A+(으)ㄴ 셈이다, V+는 셈이다::...deb hisoblash mumkin.::1년을 배웠으니 초급은 끝난 셈이에요.::1 yil o‘qiganim uchun boshlang‘ich bosqich tugadi deb hisoblayman.",
    "4B_18": "N+에 불과하다::Faqatgina ..., hech narsa emas.::그건 핑계에 불과해요.::Bu faqat bahona, xolos.",
    "4B_19": "N+만 못하다::...dan yomonroq, yaxshi emas.::이 책은 저번 책만 못해요.::Bu kitob avvalgisidek emas.",
    "4B_20": "V+(으)ㄹ 게 아니라, V+지 말고::...qilmasdan, o‘rniga...::혼자 걱정할 게 아니라 친구에게 말해요.::Yolg‘iz xavotirlanmasdan, do‘stingizga ayting.",
    "4B_21": "N+(으)로서::...sifatida (vazifa, maqom).::교사로서 학생들을 돕고 싶어요.::O‘qituvchi sifatida talabalarga yordam bermoqchiman.",
    "4B_22": "A/V+(으)므로::...gani uchun (rasmiy sabab).::비가 오므로 소풍을 취소했어요.::Yomg‘ir yog‘gani sababli sayohat bekor qilindi.",
    "4B_23": "A+다기보다는, V+ㄴ/는다기보다는::...deb bo‘lmas, ...dan ko‘ra.::실수라기보다는 고의였어요.::Bu xato emas, atay qilingan edi.",
    "4B_24": "설마 A/V+겠어요?::Nahotki..., ishonmaslik bildiradi.::설마 그 사람이 거짓말하겠어요?::Nahotki u odam yolg‘on gapirsa?",
    "4B_25": "N+(으)로부터::...dan (manba), =한테서/에게서.::부모로부터 사랑을 받았어요.::Ota-onadan mehr ko‘rdim.",
    "4B_26": "N+에 의해(서)::...orqali, sababli (rasmiy uslub).::법에 의해서 처벌받아요.::Qonunga ko‘ra jazolanadi.",
    "4B_27": "A+다고 싶다, V+ㄴ/는다고 싶다::Yumshoq istak ifodasi.::여행하고 싶다고 생각했어요.::Sayohat qilmoqchiman deb o‘yladim.",
    "4B_28": "V+곤하다::Odatdagi holat, takrorlanish.::밤에 책을 읽곤 해요.::Kechasi kitob o‘qib turaman.",
    "4B_29": "A/V+았었/었었::O‘tmishda bo‘lib, yakunlangan.::전에 갔었어요.::Oldin borgan edim.",
    "4B_30": "V+는 사이, V+는 중에, V+는 동안::...paytda, ...oratada.::공부하는 동안 조용히 해 주세요.::O‘qiyotganimda jim bo‘ling, iltimos.",
    "4B_31": "V+아/어 대다::Doimiylik yoki g‘ashga tegish.::그 사람은 계속 웃어대요.::U odam doim kulaveradi.",
    "4B_32": "N+(이)면, N+(이면)::...bo‘lsa (ifodani takrorlab kuchaytirish).::사랑이면 사랑, 우정이면 우정 모두 중요해요.::Muhabbat bo‘lsa muhabbat, do‘stlik bo‘lsa do‘stlik – barchasi muhim."
}

grammar_5A = {
    "5A_1": "5A kitobi gramatikalari tez orada qo'shiladi!!"
}

grammar_5B = {
    "5B_1": "5B kitobi gramatikalari tez orada qo'shiladi!!"
}

grammar_6A = {
    "6A_1": "6A kitobi gramatikalari tez orada qo'shiladi!!"
}

grammar_6B = {
    "6B_1": "6B kitobi gramatikalari tez orada qo'shiladi!!"
}


grammar_data = {
    "1A": grammar_1A,
    "1B": grammar_1B,
    "2A": grammar_2A,
    "2B": grammar_2B,
    "3A": grammar_3A,
    "3B": grammar_3B,
    "4A": grammar_4A,
    "4B": grammar_4B,
    "5A": grammar_5A,
    "5B": grammar_5B,
    "6A": grammar_6A,
    "6B": grammar_6B,
}


# ================= KITOB TANLANGANDA =================

@router.callback_query(F.data.startswith("book_"))
async def open_book(callback: CallbackQuery):

    book = callback.data.split("_")[1]

    grammars = grammar_data.get(book, {})

    keyboard = []

    for key in grammars.keys():
        keyboard.append([
            InlineKeyboardButton(
                text=key,
                callback_data=f"grammar_{book}_{key}"
            )
        ])

    markup = InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )

    await callback.message.edit_text(
        f"📘 {book} grammatikalari:",
        reply_markup=markup
    )

    await callback.answer()


# ================= GRAMMATIKA OCHISH =================

@router.callback_query(F.data.startswith("grammar_"))
async def show_grammar(callback: CallbackQuery):

    parts = callback.data.split("_")

    book = parts[1]
    grammar_key = "_".join(parts[2:])

    grammars = grammar_data.get(book, {})

    grammar_text = grammars.get(
        grammar_key,
        "Topilmadi ❌"
    )

    await callback.message.answer(grammar_text)

    await callback.answer()
