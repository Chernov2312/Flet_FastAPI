import asyncio
import json
import logging
from contextlib import asynccontextmanager

import aiohttp
import flet as ft
import flet_fastapi
import requests
import uvicorn
from fastapi.openapi.models import Response
from fastapi.params import Cookie
from flet_core.border_radius import horizontal
from fastapi.responses import RedirectResponse, PlainTextResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Depends, status
from app.database.databaseCRUD import add_user, get_session, get_all_users
from app.database.engine import create_db
from app.post_zapr.aiohttp_zapr import post_data
from app.schemas.pydanticmodel import User, User_check

app = flet_fastapi.FastAPI()


async def root_main(page: ft.Page):
    if page.controls:
        page.controls.pop()
    page.title = "Вход аккаунт"
    email = ft.TextField(label="Email", hint_text="Enter your email")
    password = ft.TextField(label="Password", hint_text="Enter your password", password=True)

    async def button_register(e):
        page.route = "/register"
        await register(page)

    async def button_enter(e):
        try:
            response = await post_data(url="http://127.0.0.1:8000/check_user",
                                data=User_check(email=email.value, password=password.value).__dict__)
            if response == "true":
                page.route = "/catalog"
                await catalog(page)
            else:
                await page.add_async(ft.Text("Пользователь не найден"))
        except Exception as e:
            await page.add_async(ft.Row([ft.Text(str(e))], alignment=ft.MainAxisAlignment.CENTER,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER))


    await page.add_async(ft.Row([
        ft.Column(
            [
                ft.Row([ft.Text("Вход", size=40)]),
                ft.Row([email]),
                ft.Row([password]),
                ft.Row([ft.ElevatedButton(text="Войти", on_click=button_enter),
                        ft.ElevatedButton(text="Зарегистрироваться", on_click=button_register)])
            ])
    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER))


async def register(page: ft.Page):
    if page.controls:
        page.controls.pop()
    page.title = "Регистрация"
    first_name = ft.TextField(label="First Name", hint_text="Enter your name")
    second_name = ft.TextField(label="Second Name", hint_text="Enter your second name")
    email = ft.TextField(label="Email", hint_text="Enter your Email")
    phone_number = ft.TextField(label="Phone number", hint_text="Enter your phone_number")
    password = ft.TextField(label="Password", hint_text="Enter your password", password=True)

    async def button_register(e):
        try:
            await post_data(url="http://127.0.0.1:8000/add_new_user",
                            data=User(first_name=first_name.value, second_name=second_name.value, email=email.value,
                                      phone_number=phone_number.value, password=password.value).__dict__)
            page.route = "/catalog"
            await catalog(page)
        except Exception as e:
            await page.add_async(ft.Row([ft.Text(str(e))], alignment=ft.MainAxisAlignment.CENTER,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER))

    await page.add_async(ft.Row([
        ft.Column(
            [
                ft.Row([ft.Text("Регистрация", size=40)]),
                ft.Row([first_name]),
                ft.Row([second_name]),
                ft.Row([email]),
                ft.Row([phone_number]),
                ft.Row([password]),
                ft.Row([ft.ElevatedButton(text="Продолжить", on_click=button_register)])
            ])
    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER))


async def catalog(page: ft.Page):
    if page.controls:
        page.controls.pop()
    page.title = "Каталог"
    await page.add_async(ft.Text("Вы успешно зарегистрированы"))


@app.post("/add_new_user")
async def register_post(user: User, session: AsyncSession = Depends(get_session)):
    await add_user(session=session, data=user)
    return {"massage": "complete"}


@app.post("/check_user")
async def check_user_post(user_check: User_check, session: AsyncSession = Depends(get_session)) -> bool:
    for user in await get_all_users(session):
        if user.email == user_check.email and user.password == user_check.password:
            return True
    return False


async def main():
    await create_db()
    app.mount("/login", flet_fastapi.app(root_main))


asyncio.run(main())
uvicorn.run(app, host="127.0.0.1", port=8000)
