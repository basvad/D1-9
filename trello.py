import requests  
import sys

# Данные авторизации в API Trello  
auth_params = {    
    'key': "",    
    'token': "", }  
#Доска 
board_id = ""
 
# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"  

def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        # добавляем количество задач
        print(column['name']," ",len(task_data))    
        if not task_data:    
            print('\t' + 'Нет задач!')      
            continue   
        for task in task_data:      
            print('\t' + task['name']) 
#функция создания колонок
def column_create (column_name):
# Создадим колонку с именем column_name 
# Получаем  данные  доски
    board_data = requests.get(base_url.format('boards') + '/' + board_id , params=auth_params).json() 
    requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard':board_data['id'],**auth_params})

# функция создания задач
def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    #список  для хранения задач
    list_task = [] 
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:
            #получаем все задачи в колонке
            task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
            #вытаскиваем задачи в массив
            arr_task = []
            for task in task_data: 
               arr_task.append(task['name'])
            #в завимости от нахождения задачи в массиве делаем действие
            if name in arr_task:     
                print("Задача уже имеется в данной колонке")
                break
            else:
                # Создадим задачу с именем _name_ в найденной колонке      
                requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})      
                break
            
def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
       
    # Среди всех колонок нужно найти все задачи по имени и получить их id  
    # делаем список под задачи  
    task_id = []    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:
                #добавляем в список задач    
                task_id.append(task['id']+':'+column['name']) 
                #print(task_id)      
        #if task_id:    
        #    break    
       
    # Теперь, когда у нас есть список id задач, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:
            if len(task_id)!=0:
                if len(task_id)==1:    
                     # И выполним запрос к API для перемещения задачи в нужную колонку    
                     requests.put(base_url.format('cards') + '/' + task_id[0].split(":")[0] + '/idList', data={'value': column['id'], **auth_params})    
                     break
                else:
                    print("Найдены одинаковые задачи '{}': {}".format(name,len(task_id)))
                    for i in range(len(task_id)):
                        #разбиваем запись на id и название доски
                        j=task_id[i].split(":")
                        print(i+1,' id:',j[0],' Название доски:',j[1])
                    print('Введите номер (1,2, и т.д.) задачи, которую требуется перенести:')
                    number = int(input())
                    requests.put(base_url.format('cards') + '/' + task_id[number-1].split(":")[0] + '/idList', data={'value': column['id'], **auth_params})
                    break 
            else:
                break
if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])  
    elif sys.argv[1] == 'column_create':    
        column_create(sys.argv[2])