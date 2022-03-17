#!/home/kevin/anaconda3/envs/drime/bin python
# -*-coding:utf-8 -*-
import click
import task
@click.group()
def drime():
    pass

@click.command()
@click.argument('value',nargs=2)
def add(value):
    global t1
    t1.add_task(value)

@click.command()
@click.argument('id',type=int)
def delete(id):
    global t1
    t1.delete_task(id)

@click.command()
@click.argument('id',type=int)
@click.argument('value',nargs=2)
def change(id,value):
    global t1
    t1.change_task(id,value)

@click.command()
def ls():
    global t1
    t1.list_tasks()

@click.command()
def list():
    global t1
    t1.list_tasks()

@click.command()
def status():
    global t1
    t1.status()


@click.command()
@click.option('-s/-d',default=True)
@click.argument('id',type=int)
def start(id,s):
    if s:
        t1.start_task(id)
    else:
        t1.start_task_silent(id)

@click.command()
def stop():
    t1.stop_all_task()

drime.add_command(add)
drime.add_command(delete)
drime.add_command(change)
drime.add_command(start)
drime.add_command(stop)
drime.add_command(ls)
drime.add_command(list)
drime.add_command(status)

if __name__=='__main__':
    t1=task.tasks()
    drime()