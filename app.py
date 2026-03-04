import streamlit as st
from openai import OpenAI

st.title("Конкурентный Анализатор")

# Поле для ввода API-ключа (каждый вводит свой)
api_key = st.text_input("Введи свой API-ключ OpenAI (начинается с sk-)", type="password")

if not api_key:
    st.warning("Введите свой API-ключ OpenAI, чтобы начать анализ.")
    st.info("Получить ключ: https://platform.openai.com/api-keys")
    st.stop()

# Создаём клиента только после ввода ключа
client = OpenAI(api_key=api_key)

model = "gpt-4o"  # или "gpt-4o-mini" если хочешь дешевле

# Твой промпт без изменений
base_prompt = """
Я тебе скину промт в котором будут пункты на которые ты должен будешь провести анализ по интернету. 
1.1 Страна, регион/город 
1.2 Работает ли по всей стране или же локально (это важно смотри на тематику/доставку/выезд по стране/региону) 
1.3 Топ 10 точных запросов в месяц в Яндекс Вордстат (если это сайты РФ или Белоруссии) или ads.google (если сайты Узбекские и Казахские) так же смотри внимательно на тематику сайты а не на домен и еще давай топ запросы только по городу или региону но если доставка по стране/онлайн услуги то давай запросы по стране так же напиши это в столбик с количеством просмотров в месяц если информации нету то дай топ 10 фраз для запроса что бы я сам проверил 
1.4 Далее ищешь самых ближайших прямых конкурентов у которых есть живые рабочие сайты с подходящей тематикой (город/область и на крайний случай по стране ) так же смотри на то чтобы конкуренты были одинаковой силы (пример наш сайт это команда из 10 человек а конкурент компания со штатом сотрудников из 10 тыщ.) так же не когда не бери за конкурентов доски обьявлений и государственные учериждения 
1.5 Укажи какие мессенджеры подойдут для нашего сайты для привлечения клиентов и т.д в процентном отображении из топ 10 (но обрати внимание что в РФ заблокированы многие мессенджеры их ты не указываешь и так во всех странах ) (так же смотри на нишу подойдет или данный мессенджер/площадка) 
1.6 Делаешь все то же самое что в пункте 1.5 но с площадками пример авито  
1.7 выдай сайты конкурентов именно ссылкой штук 10 то есть топ 10 
1.8 в самом начале напиши это коммерческий или некоммерческий это тоже важно 
1.9 ничего не додумывай основываясь только на той информации которая есть в интернете (если есть противоречия напиши их рядом с коммерческий  ) 
и если меня что то не устроит из пунктов я буду тебе писать пункт который нужно переделать (только то пункт который я укажу)
"""

domain = st.text_input("Введи домен сайта (например, example.com):")

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = ""
if 'refine' not in st.session_state:
    st.session_state.refine = False

if st.button("Провести анализ"):
    if domain:
        with st.spinner("Анализ выполняется..."):
            try:
                full_prompt = base_prompt + f"\n\nАнализируй этот домен: {domain}"
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": full_prompt}]
                )
                st.session_state.analysis_result = response.choices[0].message.content
                st.session_state.refine = False
            except Exception as e:
                st.error(f"Ошибка: {str(e)}. Проверь ключ, баланс или интернет.")
    else:
        st.warning("Введи домен сначала!")

if st.session_state.analysis_result:
    st.subheader("Результат анализа от ИИ:")
    st.text_area("Подробный анализ:", st.session_state.analysis_result, height=500)

if st.session_state.analysis_result and st.button("Переанализировать (более точно)"):
    with st.spinner("Переанализ выполняется..."):
        try:
            refine_prompt = base_prompt + f"\n\nАнализируй этот домен: {domain}\nПредыдущий анализ: {st.session_state.analysis_result}\nПереанализируй более детально и точно, исправь ошибки, основываясь только на интернете."
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": refine_prompt}]
            )
            st.session_state.analysis_result = response.choices[0].message.content
            st.session_state.refine = True
        except Exception as e:
            st.error(f"Ошибка: {str(e)}.")

if st.session_state.refine:
    st.info("Анализ был уточнён на основе предыдущего!")