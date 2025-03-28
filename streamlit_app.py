import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

op_stat = '''
<h1>Статистика на основе данных людей, находившихся на титанике
<h2>Описательная статистика</h2>
<p>В нащем распоряжении таблица с данными о количестве людей, которые находились на титанике,
состоящая из <strong>12 столбцов и 891 строк.</strong></p> 
В таблице представлены следующие столбцы: 
<dl>
<dt><strong>Passengerld</strong></dt>
<dd>Нумерация пассажиров, целые числа</dd>
<dt><strong>Survied</strong></dt>
<dd>Характеризует, выжил ли данный пассажир (целочисленный тип данных): 
<ul>
<li><strong>0</strong> - не выжил</li> 
<li><strong>1</strong> - выжил</li> 
</ul>
</dd>
<dt><strong>Pclass</strong></dt>
<dd>Класс обслуживания, обозначается целыми числами
<ul>
<li><strong>1</strong> - высший класс с роскошными каютами, доступом к эксклюзивным зонам и высокими тарифами</li> 
<li><strong>2</strong> - средний класс с комфортными условиями, но без роскоши первого</li>
<li><strong>3</strong> - низший класс с базовыми условиями, преобладал среди пассажиров (491 человек против 216 и 184 в первом и втором классах соответственно)</li> 
</ul>
</dd>
<dt><strong>Name</strong></dt>
<dd>Имя, строковый тип данных</dd>
<dt><strong>Sex</strong></dt>
<dd>Пол, строковый тип данных</dd>
<dt><strong>Age</strong></dt>
<dd>Возраст, целые числа</dd>
<dt><strong>SibSp</strong></dt>
<dd>Количество братьев и сестер или супругов, которые находились на корабле вместе с пассажиром, целые числа</dd>
<dt><strong>Parch</strong></dt>
<dd>Количество родителей или детей, которые находились на корабле вместе с пассажиром, целые числа</dd>
<dt><strong>Ticket</strong></dt>
<dd>Номер билета, строковый тип данных</dd>
<dt><strong>Fare</strong></dt>
<dd>Стоимость билета, вещественные числа</dd>
<dt><strong>Cabin</strong></dt>
<dd>Обозначает номер каюты, где жил пассажир, строковый тип данных</dd>
<dt><strong>Embarked</strong></dt>
<dd>порт посадки, где пассажир сел на корабль
<ul>
<li><strong>C</strong> - Cherbourg (Шербур, Франция)</li> 
<li><strong>Q</strong> - Queenstown (Куинстаун, Ирландия)</li>
<li><strong>S</strong> - Southampton (Саутгемптон, Англия)</li> 
</ul>
</dd>
</dl>
'''

st.write(op_stat,  unsafe_allow_html=True)
df = pd.read_csv('titanic.csv')
st.write(len(df.columns))
df
# Обработка данных
mini_df = df[['Age','SibSp']].dropna().reset_index(drop=True)

st.write("<p><strong>Зависимость количества родственников от возраста</strong></p>", unsafe_allow_html=True)
# График зависимости между Age и SibSp
st.scatter_chart(mini_df, x='Age', y='SibSp')
# ## Преобразование Cabin в бинарный признак
# df['Has_Cabin'] = df['Cabin'].notna().astype(int)




# Фильтрация данных по выбранному полу
selected_sex = st.selectbox(
    "Выберите пол:",
    options=df['Sex'].unique(),
    index=0  # По умолчанию показываем мужчин
)

filtered_df = df[df['Sex'] == selected_sex].dropna(subset=['Pclass', 'Survived'])

# Группировка данных по классу каюты и статусу выживания
status_counts = filtered_df.groupby(['Pclass', 'Survived']).size().reset_index(name='Количество')

# Построение графика с группированными столбиками
fig = px.bar(
    status_counts,
    x='Pclass',
    y='Количество',
    color='Survived',
    barmode='group',
    color_discrete_sequence=['red', 'green'],  # Красный для погибших, зелёный для выживших
    labels={
        'Pclass': 'Класс каюты',
        'Survived': 'Статус',  # Будет заменён на 0 и 1
        'Количество': 'Количество пассажиров'
    },
    title=f"Количество погибших и выживших по классу каюты ({selected_sex})",
    category_orders={'Survived': [0, 1]}  # Упорядочиваем статусы (0 → 1)
)

# Настройка легенды
fig.update_layout(
    legend=dict(
        title=None,  # Убираем заголовок "Статус"
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# Вывод графика в Streamlit
st.plotly_chart(fig)




# Создание признака "Наличие каюты"
df['Has_Cabin'] = df['Cabin'].notna().astype(int)

# Группировка данных
cabin_counts = df.groupby(['Has_Cabin', 'Survived']).size().reset_index(name='Количество')

# Построение графика
fig = px.bar(
    cabin_counts,
    x='Has_Cabin',
    y='Количество',
    color='Survived',
    barmode='group',
    color_discrete_sequence=['red', 'green'],
    labels={
        'Has_Cabin': 'Наличие каюты\n(1 — есть, 0 — нет)',
        'Survived': 'Статус выживания',
        'Количество': 'Количество пассажиров'
    },
    title='Выживаемость в зависимости от наличия каюты'
)

# Настройка легенды
fig.update_layout(
    legend=dict(
        title=None,
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# Вывод графика
st.plotly_chart(fig)




# Гистограмма возрастов
st.subheader("Распределение возрастов пассажиров")
age_hist = df[['Age']].dropna()
fig = px.histogram(age_hist, x='Age', nbins=20, title='Распределение возрастов')
fig.update_layout(xaxis_title='Возраст', yaxis_title='Количество пассажиров')
st.plotly_chart(fig, key="age_hist")





# Интерактивный график с фильтрами
st.subheader("Интерактивный анализ выживаемости")
filtered_df = df.dropna(subset=['Age', 'Fare', 'Pclass', 'Survived'])

# Фильтры
selected_sex = st.selectbox("Выберите пол", df['Sex'].unique())
selected_pclass = st.selectbox("Выберите класс каюты", df['Pclass'].unique())

filtered_df = filtered_df[
    (filtered_df['Sex'] == selected_sex) &
    (filtered_df['Pclass'] == selected_pclass)
]

# График с цветами и именами
fig = px.scatter(
    filtered_df,
    x='Age',
    y='Fare',
    color='Survived',
    hover_name='Name',
    hover_data=['Sex', 'Pclass'],
    labels={'Age': 'Возраст', 'Fare': 'Тариф'}
)

# Применяем цвета напрямую
fig.update_traces(
    marker=dict(
        color=['#FF0000' if x == 0 else '#00FF00' for x in filtered_df['Survived']]
    )
)

# Настройка ховер-информации
fig.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>" +
                  "Возраст: %{x}<br>" +
                  "Тариф: %{y}<br>" 
)

# Добавляем данные для кастомного ховер
fig.update_traces(customdata=[filtered_df[['Sex', 'Pclass']].values.tolist()])

fig.update_layout(
    title='Выживаемость по возрасту и тарифу',
    legend=dict(
        title=None,
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)
st.plotly_chart(fig, key="interactive_scatter")




# Слайдер для выбора количества строк
x = st.slider('Количество строк', min_value=1, max_value=len(df), value=5)

# Вывод таблицы с выбранным количеством строк
st.write(df.head(x))
