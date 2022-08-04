from website.wsgi import *
import csv
from core.models import *
import re

def padrao1(numero: str):
    """(99)99999-9999"""
    finder = re.compile(r'[(]\d\d[)]\d\d\d\d\d-\d\d\d\d')
    return finder.findall(numero)


def tck(numero: str):
    """99999999999"""
    finder = re.compile(r'\d\d\d\d\d\d\d\d\d\d\d')
    return finder.findall(numero)


def padrao2(numero: str):
    """(99)9 9999-9999"""
    finder = re.compile(r'[(]\d\d[)]\d \d\d\d\d-\d\d\d\d')
    return finder.findall(numero)


def padrao3(numero: str):
    """(99) 99999-9999"""
    finder = re.compile(r'[(]\d\d[)] \d\d\d\d\d-\d\d\d\d')
    return finder.findall(numero)


def padrao4(numero: str):
    """(99) 9 9999-9999"""
    finder = re.compile(r'[(]\d\d[)] \d \d\d\d\d-\d\d\d\d')
    return finder.findall(numero)


def padrao5(numero: str):
    """(99)9999-9999"""
    finder = re.compile(r'[(]\d\d[)]\d\d\d\d-\d\d\d\d')
    return finder.findall(numero)


def padrao6(numero: str):
    """(99) 9999-9999"""
    finder = re.compile(r'[(]\d\d[)] \d\d\d\d-\d\d\d\d')
    return finder.findall(numero)


def padrao7(numero: str):
    """99999-9999"""
    finder = re.compile(r'\d\d\d\d\d-\d\d\d\d')
    return finder.findall(numero)


def padrao8(numero: str):
    """9999-9999"""
    finder = re.compile(r'\d\d\d\d-\d\d\d\d')
    return finder.findall(numero)


with open('final.csv', 'r') as file:
    leitor = csv.reader(file)
    for i, n in enumerate(leitor):
        if i > 0:
            nome = n[0]
            resp = n[1]
            email = n[2]
            telefone1 = n[3]
            telefone2 = n[4]
            ticket = n[5]
            produto = n[6]
            emissao = n[7]
            validade = n[8]
            v = n[9]
            if '.' not in v:
                valor = '0'
            else:
                valor = v
            obs = n[10]

            try:
                cli = Cliente.objects.get(nome=nome)
                certificado = Certificado(
                    cliente=cli,
                    ticket=ticket,
                    produto=produto,
                    emissao=emissao,
                    validade=validade,
                    valor=valor,
                    observacao=obs
                )
                certificado.save()
            except:
                cli = Cliente(
                    nome=nome,
                    responsavel=resp,
                    email=email,
                    telefone1=telefone1,
                    telefone2=telefone2,
                )
                cli.save()
                certificado = Certificado(
                    cliente=cli,
                    ticket=ticket,
                    produto=produto,
                    emissao=emissao,
                    validade=validade,
                    valor=valor,
                    observacao=obs
                )
                certificado.save()
