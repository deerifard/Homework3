# Конфигурационнон управление - Домашнее задание 3
## Общее описание 

Разработать инструмент командной строки для учебного конфигурационного языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из входного формата в выходной. Синтаксические ошибки выявляются с выдачей сообщений.  

Входной текст на языке xml принимается из стандартного ввода. Выходной текст на учебном конфигурационном языке попадает в стандартный вывод.  

Однострочные комментарии:  

|| Это однострочный комментарий 

Многострочные комментарии:  

{- 

Это многострочный 

комментарий -}  

Массивы: 

( значение, значение, значение, ... )   

Словари: 

$[ 

имя : значение, 

имя : значение, 

имя : значение, 

... 
]  

Имена: 

[_a-z]+  

Значения: 

• Числа. 

• Массивы. 

• Словари.  

Объявление константы на этапе трансляции: 

def имя := значение 

Вычисление константного выражения на этапе трансляции (постфиксная форма), пример: 

?{имя 1 +}  

Результатом вычисления константного выражения является значение.  

Для константных вычислений определены операции и функции: 

1. Сложение.

2. mod().
   
Все конструкции учебного конфигурационного языка (с учетом их возможной вложенности) должны быть покрыты тестами. Необходимо показать 2 

примера описания конфигураций из разных предметных областей.
