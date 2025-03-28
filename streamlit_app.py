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
st.dataframe(df.describe())



# Создание признака "Наличие каюты"
df['Has_Cabin'] = df['Cabin'].notna().astype(int)

# Группировка данных
cabin_counts = df.groupby(['Has_Cabin', 'Survived']).size().reset_index(name='Количество')

# Переименовываем значения, чтобы легенда была понятнее
cabin_counts['Survived'] = cabin_counts['Survived'].map({0: 'Погиб', 1: 'Выжил'})

# Определяем цвета для легенды
colors = {'Погиб': 'red', 'Выжил': 'green'}

# Построение графика
fig = px.bar(
    cabin_counts,
    x='Has_Cabin',
    y='Количество',
    color='Survived',
    barmode='group',
    color_discrete_map=colors,  # Задаем цвета для легенды
    labels={
        'Has_Cabin': 'Наличие каюты\n(1 — есть, 0 — нет)',
        'Survived': 'Статус выживания',
        'Количество': 'Количество пассажиров'
    },
    title='Выживаемость в зависимости от наличия каюты в таблице'
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
    ),
    coloraxis_showscale=False  # Убираем градиент
)

# Вывод графика
st.plotly_chart(fig)




# Обработка пропущенных значений
df_no_na = df.dropna(subset=['Age', 'SibSp'])

# Создание графика "ящик с усами"
fig = px.box(
    df_no_na,
    x="Age",  # Возраст по горизонтали
    y="SibSp",  # Количество родственников по вертикали
    orientation='h',  # Горизонтальное расположение ящиков
    title="Зависимость количества родственников от возраста",
    labels={"SibSp": "Количество родственников", "Age": "Возраст"},
)

# Настройка графика (необязательно)
fig.update_layout(
    yaxis=dict(title_standoff=25)  # Отступ для названия оси Y
)


# Вывод графика в Streamlit
st.plotly_chart(fig)




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




# Создаем копию датафрейма без пропусков
mini_df = df[['Age', 'Fare', 'SibSp', 'Survived', 'Name', 'Sex']].dropna()

# Назначаем цвета в зависимости от выживания
mini_df['Color'] = mini_df['Survived'].map({0: 'погиб', 1: 'выжил'})

# Создаем 3D-график без цветовой шкалы
fig = px.scatter_3d(
    mini_df,
    x='Age',
    y='Fare',
    z='SibSp',
    color= 'Color',
    hover_data=['Name', 'Sex'],
    title='Выживаемость в зависимости от возраста, стоимости билета и родственников',
    labels={
        'Age': 'Возраст',
        'Fare': 'Стоимость билета',
        'SibSp': 'Количество родственников',
        'Color': 'Выжил'
    }
)


# Настройка размера и цвета точек
fig.update_traces(
    marker=dict(
        size=3,  # Маленькие точки
        line=dict(width=0.5, color='DarkSlateGrey'),  # Чёрная обводка
        opacity=0.8  # Прозрачность
    )
)

# Скрываем цветовую шкалу
fig.update_layout(
    coloraxis_showscale=False,
    scene = dict(
        xaxis_title='Возраст',
        yaxis_title='Стоимость билета',
        zaxis_title='Количество родственников'
    ),
    width=800,
    height=600,
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Arial"
    )
)

# Отображение графика
st.plotly_chart(fig)



# Слайдер для выбора количества строк
x = st.slider('Количество строк', min_value=1, max_value=len(df), value=5)

# Вывод таблицы с выбранным количеством строк
st.write(df.head(x))




