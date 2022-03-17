#!/home/kevin/anaconda3/envs/drime/bin python
# -*-coding:utf-8 -*-
import os
import prettytable
import progressbar
import time
class tasks():
    '''
    task具有三个属性：任务，剩余时间，总时间
    '''
    def __init__(self,save_location='${HOME}/Documents/codes/drime/data/tasks.txt'):
        self.tasks=[]
        self.save_location=save_location
        self.start_time=0
        self.current_task_id=-1
        self.init_tasks()

    
    # def __del__(self):
    #     self.write_tasks()

    def init_tasks(self):
        '''
        从本地保存路径中读取任务，如果指定路径没有该文件则自动创建
        '''
        if os.path.exists(self.save_location):
            with open(self.save_location,encoding='utf-8',mode='r') as f:
                lines=f.readlines()
            self.current_task_id=int(lines[0].strip())
            self.start_time=float(lines[1].strip())
            for i in range(2,len(lines)):
                task=lines[i].rstrip('\n').split('$$$$$$')
                if len(task)>=3:
                    task[1]=float(task[1])
                    task[2]=float(task[2])
                    self.tasks.append(task)
        else:
            open(self.save_location,'a').close()
    
    def list_tasks(self):
        '''
        打印任务列表
        '''
        table=prettytable.PrettyTable(['序号','任务','剩余时间','总时间'])
        self.update_current_task_remain_time()
        try:
            for i in range(len(self.tasks)):
                table.add_row([i+1,self.tasks[i][0],self.second2time_stamp(self.tasks[i][1]),self.second2time_stamp(self.tasks[i][2])])
            print(table)
            return 0
        except:
            print('打印任务列表出错！/n')
            return 1

    def add_task(self,task):
        '''
        task形如[xx任务,'xxhxxmxxs']
        '''
        if len(task)==2:
            total_time=self.time_stamp2second(task[1])
            if total_time==None:
                print('输入时间格式有误！\n')
                return 1
            self.tasks.append([task[0],total_time,total_time])
            self.write_tasks()
            print('任务添加成功！\n')
            return 0
        else:
            print('任务参数输入有误！\n')
            return 1

    def change_task(self,i,new_task):
        '''
        将第i-1条任务修改为new_task
        new_task形如[任务，总时间]
        '''
        if isinstance(i-1,int) and i>0:
            if len(new_task)==2:
                total_time=self.time_stamp2second(new_task[1])
                if total_time==None:
                    print('输入时间格式有误！\n')
                    return 1
                self.tasks[i-1][0]=new_task[0]
                used_time=self.tasks[i-1][2]-self.tasks[i-1][1]
                self.tasks[i-1][2]=total_time
                self.tasks[i-1][1]=total_time-used_time
                self.write_tasks()
                return 0
            else:
                print('任务参数输入有误！\n')
        else:
            print("任务id输入错误!\n")
            return 1
    
    def delete_task(self,i):
        '''
        删除第i-1条任务
        '''
        if isinstance(i-1,int) and i>0:
            if i-1==self.current_task_id:
                print('当前任务正在进行，无法删除！')
            else:
                self.tasks.pop(i-1)
                self.write_tasks()
                return 0
        else:
            print("任务id输入错误!\n")
            return 1

    def write_tasks(self):
        '''
        将self.tasks中保存的任务写入本地保存的文件中
        '''
        tasks_txt=""
        tasks_txt+=str(self.current_task_id)+'\n'
        tasks_txt+=str(self.start_time)+'\n'
        for task in self.tasks:
            tasks_txt+=task[0]+'$$$$$$'+str(task[1])+'$$$$$$'+str(task[2])+'\n'
        with open(self.save_location,encoding='utf-8',mode='w') as f:
            f.write(tasks_txt)
    
    def time_stamp2second(self,time_stamp):
        '''
        时间戳转化为秒
        '''
        hour=0
        minute=0
        second=0
        try:
            if 'h' in time_stamp:
                [hour,time_stamp]=time_stamp.split('h')
            if 'm' in time_stamp:
                [minute,time_stamp]=time_stamp.split('m')
            if 's' in time_stamp:
                second=time_stamp.split('s')[0]
        except:
            return None
        seconds=3600*int(hour)+60*int(minute)+int(second)
        return seconds
    
    def second2time_stamp(self,seconds):
        '''
        秒转化为时间戳
        '''
        hour=0
        minute=0
        second=0
        if seconds>3600:
            hour=int(seconds/3600)
            seconds=seconds%3600
        if seconds>60:
            minute=int(seconds/60)
            seconds=seconds%60
        time_stamp=''
        if hour>0:
            time_stamp+=str(hour)+'h'
        if minute>0:
            time_stamp+=str(minute)+'m'
        if second!=0:
            time_stamp+=str(second)+'s'
        return time_stamp
            
    
    def start_task_silent(self,task_id):
        '''
        开启task_id-1个任务的计时
        '''
        if isinstance(task_id-1,int) and task_id>0:
            task=self.tasks[task_id-1]
            self.current_task_id=task_id-1
            self.start_time=time.time()
            self.write_tasks()
        else:
            print("任务id输入错误!\n")
            return 1
    
    def show_current_task_progressbar(self):
        '''
        显示当前进行任务的进度条
        '''
        if self.current_task_id!=-1:
            remain_time=self.tasks[self.current_task_id][1]
            remain_time=int(remain_time-(time.time()-self.start_time))
            bar = progressbar.ProgressBar(
                widgets=[
                    progressbar.ETA(),
                    progressbar.Bar(),
                ],
            )
            print('当前正在进行：任务'+str(self.current_task_id+1)+' '+self.tasks[self.current_task_id][0])
            for i in bar(range(10*remain_time)):
                time.sleep(0.1)
        else:
            print('当前没有在进行任何任务')
            return 0
    
    def start_task(self,task_id):
        '''
        开启第task_id-1个任务的计时，并显示当前进行任务的进度条并
        '''
        if self.start_task_silent(task_id)!=1:
            self.show_current_task_progressbar()
            return 0
        else:
            return 1

    def update_current_task_remain_time(self):
        '''
        更新当前进行任务的剩余时间
        '''
        if self.current_task_id!=-1:
            now_time=time.time()
            self.tasks[self.current_task_id][1]=self.tasks[self.current_task_id][1]-(now_time-self.start_time)
            self.start_time=now_time
            self.write_tasks()
        return 0


    def stop_all_task(self):
        '''
        停止当前正在进行的任务
        '''
        if self.current_task_id!=-1:
            self.update_current_task_remain_time()
            self.current_task_id=-1
            self.write_tasks()
        return 0
    
    def clear_tasks(self):
        self.tasks=[]
        self.write_tasks()
    
    def status(self):
        if self.current_task_id!=-1:
            self.show_current_task_progressbar()
        else:    
            print('当前没有在进行任何任务')
        return 0
    

if __name__=='__main__':
    t1=tasks()
    t1.add_task(['写作业','20m'])
    t1.list_tasks()
    t1.change_task(1,['写生物作业','15m'])
    t1.list_tasks()