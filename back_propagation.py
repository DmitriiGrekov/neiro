"""
Алгоритм обучения с обратным распространением ошибки

Для нахождения весовых коэффициентов необходим следующий алгоритм.
Картинка backpropagation.png
Есть 2 входа x1 и x2, есть веса связи которые выбираются в произвольном образом в [-0.5, 0.5]
У каждого нейрона имеется активационная функция f(x)
Также есть наблюдения которые мы будем подавать на вход нейронной сети и будем обозначать как d(это правильные варианты для обучения)
Мы подаем на вход конкретные наблюдения (вектор x1,x2), рассчитываем значение каждого нейрона v11, v12, v13 (к примеру v11 = x1*w11 + x2*w12)
Дальше рассчитываем функцию активации для каждого нейрона, и значение функции активации будет передаваться на следующий слой нейронной сети.
И так для каждого слоя, и в конце концов получаем y (фото backpropagation2.png). Зная d и y мы можем вычислить ошибку e = y - d

В соответсвии с алгоритмом обратного распространения ошибки, первое что нам нужно сделать, это вычислить градиент для выходного нейрона
δ = e * f`(vout)
f` - значение производной функции активации.

Для нейросетей с небольшим числом слоев часто применяют следующие активационные функции: Гиперболический тангенс или логистическая функция (фото backpropagation3.png)
В зависимости от того, какой уровень выходной функции ннам нужен(тоесть либо от -1 до 1, либо от 0 до 1) ту и выбираем

Если мы выбираем логистическую функцию, то ее производная будет равна:
f`(x) = f(x) * (1-f(x))
Следовательно
δ = e * f`(vout) = e * f(vout) * (1-f(vout))
Если y = f(vout)
δ = e * y (1-y)
Формула для корреции весов w11(3) представлена на рисунке backpropagation4.png
w11(3) = w11(3) - (шаг сходимости алгоритма обучения * логальный градиент δ * выходной сигнал f21)

для нейрона 2 слоя v21, v22 необходимо знать значение его локального градиента, для этого необходимо взять локальный градиент δ для последнего нейрона
и прогоняем его через веса связи w11(3) и w12(3)

получим 
δ21 = δ*w11(3) *f`(v21) = δ*w11(3)*[f21*(1-f21)]
δ22 = δ*w12(3) *f1(v22) = δ*w12(3)*[f22*(1-f22)]

Скорректированные веса для нейронов 2 слоя с конца изображены на рисунке backpropagation5.png
Скорректированные веса для первого слоя изображены на рисунке backprogataiont6.png
 
Критерий качества работы нейронной сети представлен на изображении backpropagation7.png

Активационная функция Гиперболический тангенс
f(x) = 2/(1+e^x) - 1
f`(x) = 1/2 *(1+f(x))*(1-f(x))
"""

import numpy as np

def f(x):
    """Гиперболический тангенc"""
    return 2/(1+np.exp(-x)) - 1


def df(x):
    """Производная гиперболического тангенса"""
    return 0.5 * (1+x)*(1-x)


# Веса нейронной сети
W1 = np.array([[-0.2, 0.3, -0.4], [0.1, -0.3, -0.4]])
W2 = np.array([0.2, 0.3])


def do_forward(inp):
    """Расчет выходного значения нейронной сети"""
    sum = np.dot(W1, inp)
    out = np.array([f(x) for x in sum])

    sum = np.dot(W2, out)
    y = f(sum)
    return (y, out)


def train(epoch):
    """Обучение нейронной сети"""
    global W2, W1
    lmd = 0.01 # шаг обучения
    N = 10000 # число итераций при обучении
    count = len(epoch)
    for k in range(N):
        x = epoch[np.random.randint(0, count)] # случайный выбор входного сигнала из обучающей выборки
        y, out = do_forward(x[0:3]) # прямой проход по НС и вычислени выходных значений нейронной сети
        e = y - x[-1] # ошибка
        delta = e * df(y) # локальный градиент
        W2[0] = W2[0] - lmd * delta * out[0] # корректировка веса первой связи
        W2[1] = W2[1] - lmd * delta * out[1] # корректировка веса второй связи
        delta2 = W2*delta*df(out)

        # корректировка связей первого слоя
        W1[0, :] = W1[0, :] - np.array(x[0:3]) * delta2[0] * lmd
        W1[1, :] = W1[1, :] - np.array(x[0:3]) * delta2[1] * lmd


# обучающая выборка (она же полная выборка)

epoch = [(-1, -1, -1, -1), # первые 3 параметра это входной вектор а последний это требуемое значение
         (-1, -1, 1, 1),
         (-1, 1, -1, -1),
         (-1, 1, 1, 1),
         (1, -1, -1, -1),
         (1, -1, 1, 1),
         (1, 1, -1, -1),
         (1, 1, 1, -1)]


train(epoch) # запуск обучения сети

# проверка полученных результатов
for x in epoch:
    y, out = do_forward(x[0:3])
    print(f'Выходное значение НС: {y} => {x[-1]}')



"""
Рекомендация обучения №1: Запускать алгоритм для разных начальных значений весовых коэффициентов. И, затем, отобрать лучший вариант.
Начальные значения генерируем случайным образом в окрестности нуля, кроме тех, что относятскся к bias'ам

Bias отвечает за смещение гиперплоскости, и к нему это правило не относится.

Другая проблема градиентного спуска, это медленная сходимость на пологих участках (рисунок backpropagation8.png). 
Для решения этой проблемы чаще всего используются методы оптимизации Нестерова и Adam.

Рекомендация обучения №2: запускаем алгоритм обучения с оптимизацией по Adam или Нестерову для ускорения обучения НС.


Как правильно подавать входные значения на входа НС

Предположим что у нас есть N векторов и для каждого требуемый отклик (рисунок backpropagation9.png).
Стоит ли передавать вектор содержащий все xi...xl. На самом деле не стоит, потому что в общем случае из xi..xl могут быть большие значения
которые приведут в область насыщения функции активации (рисунок backpropagation10.png)
На практике значения xi...xl стандартизируют по формуле:

(xi - min)/(max-min), где min, max - минимальное и максимальное значение по всей выборке всех векторов, на выходе получаем значение [0, 1]

Если сеть обучается на нормированных значения, то данные при её работе нужно также нормировать при тех же значениях min и max.

Рекомендация обучения №3: выполнять нормировку входных значений и запоминать нормировочные параметры min, max из обучающей выборки

Рекомендация обучения №5: Наблюдения на вход сети подавать случайным образом, корректировать вес после серии наблюдений, разбитых по mini-batch.


Q - критерий качества работы НС. Если он нас не устраивает, вся выборка опять тасуется и опять происходит обучение НС.
"""


"""
ПЕРЕОБУЧЕНИЕ

Чем больше нейронов в скрытом слое, тем сложнее вид разделяющей линии(получается кривая, а когда в скрытом слое 1 нейрон то получается прямая.),
тем самым появляются дополнительные ошибки в процессе её эксплуатации - это и есть переобучение, когда разделяющая плоскость точно повторяет обучающую выборку.

Рекомендация обучения №6: Использовать минимальное необходимое число нейронов в нейронной сети

Для контроля обучения, обучающая выборка разделяется на обучающую выборку и выборку валидации и на каждой итерации подсчитываем качество ее работы
(рисунок backpropagation11.png)

Рекомендация обучения №7: разбивать все множество наблюдений на три выборки: обучающую, валидации и тестовую.

Критерии остановки процесса обучения:

1) Расхождение показателя качества для обучающей выборки и валидации.
2) От итерации к итерации (по все эпохе) показатель качества Q практически не меняется
3) Происходит малое изменение весовых коэффициентов
4) Достигли максимального числа итераций
"""


"""
Функции активации нейронов

Нам знакомы 3 функции активации (фото backpropagation12.png): пороговая функция, гиперболический тангенс и логистическая функция.
Пороговая функция используется редко, гиперболический тангенс и логистическая функция используются в НС с маленьким числом слоем (3 или 6),
потому что локальный градиент для скрытого слоя рассчитывается по формуле, изображенной на рисунке backpropagation13.png

При обучении больших НС используется функция ReLu.
Рекомендация обучения №8: При малом числе слоев можно использовать гиперболическую и сигмоидальную функции активыции или ReLu, при числе слоев от 8 и более - ReLu и ее вариации

В задачах регрессии (прогнозировании какой-либо цены, роста человека) используются функция активации linear f(x) = x

В задачах классификации у выходного слоя будет отличаться функция активации от скрытых слоев (фото backpropagation14.png)

Для выходного слоя используется активационная функция softmax.

При softmax критерием качества является перекрестная энтропия (фото backpropagation15.png)

Рекомендация обучения №9: для задач регрессии (нахождения конкретного числа) у выходных нейронов использовать линейную (linear) функция активации,
а для задач классификации не пересекающихся классов softmax.


Критерим качества для алгоритма обучения backpropagation является минимум средних квадратных значений ошибок между требуемым выходом и реальным
(фото backpropagation16.png).

Для распознавания образов лучшим критерием качества является:
1) хиндж (hinge)
2) бинарная кросс-энтроприя (binary crossentropy) - при классификации двух классов
3) категориальная кросс-энтроприя (categorical crossentropy) - при классификации более двух классов
Рисунок backpropagation18.png, backpropagation19.png, backpropagation20.png

Для обработки текста:
1) логарифмический гиперболический косинус (logcosh)
Рисунок backpropagation21.png

Для задач регрессии:
1) средний квадрат ошибок (mean squared error)
2) средний модуль ошибко (mean absolute error)
3) средний абсолютный процент ошибок (mean absolute percentage error) - хороша в прогнозировании
4) средний квадрат логарифмических ошибко (mean squared logarithmic error)

Рисунок backpropagation17.png
"""