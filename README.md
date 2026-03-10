<div align="center">
  <h1>AstraWilly</h1>
  <h3>This pet project simulates a real ISP website built with Django, mirroring the scale and functionality of a major telecom operator.</h3>
  <p>
    <a href="https://www.youtube.com/watch?v=-UHFMVFRRRc" target="_blank">
      <img src="https://img.shields.io/badge/Watch%20on-YouTube-red?style=for-the-badge&logo=youtube" alt="YouTube">
    </a>
  </p>
</div>

✨ Overview

A full‑featured multi‑language website for an internet service provider. Users can explore tariffs, services, vacancies, and news; submit applications; manage their profile; and choose how they want to be contacted. The admin panel gives full control over all content and requests.

🎯 Features

<div style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center;">
  <div style="flex: 1 1 250px; background: #f5f7fa; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <strong>🌍 Multi‑language</strong><br>
    German, English, Russian, Dutch, Ukrainian (i18n + locale middleware)
  </div>
  <div style="flex: 1 1 250px; background: #f5f7fa; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <strong>🔐 User accounts</strong><br>
    Sign up, sign in, logout, change password, password reset via email
  </div>
  <div style="flex: 1 1 250px; background: #f5f7fa; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <strong>👤 Personal cabinet</strong><br>
    View selected tariffs, services, packages; track application history
  </div>
  <div style="flex: 1 1 250px; background: #f5f7fa; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <strong>📋 Applications</strong><br>
    For vacancies, tariffs, individual services, packages, and support
  </div>
  <div style="flex: 1 1 250px; background: #f5f7fa; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <strong>📞 Contact methods</strong><br>
    Telegram, Email, Phone call, WhatsApp
  </div>
  <div style="flex: 1 1 250px; background: #f5f7fa; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <strong>💱 Currency support</strong><br>
    Auto‑updated exchange rates (Frankfurter.app); show prices in multiple currencies
  </div>
  <div style="flex: 1 1 250px; background: #f5f7fa; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <strong>📍 Location detection</strong><br>
    IP‑based country detection + manually added countries (editable in admin)
  </div>
  <div style="flex: 1 1 250px; background: #f5f7fa; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <strong>⚙️ Admin panel</strong><br>
    Full control over tariffs, services, vacancies, news, applications, countries, currencies
  </div>
  <div style="flex: 1 1 250px; background: #f5f7fa; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <strong>⏱️ Background tasks</strong><br>
    Celery + Redis for notifications, emails, and periodic currency updates
  </div>
  <div style="flex: 1 1 250px; background: #f5f7fa; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <strong>🐘 PostgreSQL</strong><br>
    Robust and scalable database
  </div>
  <div style="flex: 1 1 250px; background: #f5f7fa; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <strong>📱 Responsive design</strong><br>
    Works perfectly on desktop and mobile
  </div>
</div>


🛠 Tech Stack

| Area          | Technologies                                                                 |
|---------------|------------------------------------------------------------------------------|
| **Backend**   | Python, Django, Django ORM                                                   |
| **Database**  | PostgreSQL                                                                   |
| **Task Queue**| Celery, Redis (broker & cache)                                               |
| **Frontend**  | Django templates, Bootstrap                                                  |
| **i18n**      | Django internationalization (locale middleware)                              |
| **Geolocation**| Custom IP‑based detector + manual country list                              |
| **Currency**  | Frankfurter.app API, `requests` library                                      |

📸 Screenshots
<details>
<summary>🏠 Home Page</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" src="https://github.com/user-attachments/assets/30a6774b-eede-41d8-b920-05d74c09c9b6" alt="Home">
  <img width="48%" src="https://github.com/user-attachments/assets/3d3389fb-efbf-43c4-8229-d00c6f1ea761" alt="Home1">
  <img width="48%" src="https://github.com/user-attachments/assets/1ccff392-33a3-4dd8-9736-4434fcd413ac" alt="Homefooter">
</div>
</details>

<details>
<summary>🌐 Languages & Location</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" src="https://github.com/user-attachments/assets/ca5b1438-fe93-4dbb-9d4f-83a45c3b4f38" alt="Languages">
  <img width="48%" src="https://github.com/user-attachments/assets/80db1122-2bfd-4669-bd44-5a10e5f1ee81" alt="Countries">
</div>
</details>

<details>
<summary>📶 Tariffs</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" src="https://github.com/user-attachments/assets/07c09936-7a38-4637-9e15-f946ded51034" alt="Tariffs">
  <img width="48%" src="https://github.com/user-attachments/assets/5763e57a-3abc-43e7-a2e7-5b0ea761b13f" alt="Tariffs_1">
  <img width="48%" src="https://github.com/user-attachments/assets/2255bdf1-8502-4432-b839-14360f05cf41" alt="Tariffs_3">
  <img width="48%" src="https://github.com/user-attachments/assets/3859a429-a059-443c-b23b-d7839d83fbd5" alt="Tariffs_4">
</div>
</details>

<details>
<summary>🛠 Services</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" src="https://github.com/user-attachments/assets/854e0ae1-10ea-4eb6-bd47-d85a6cab1977" alt="Services">
  <img width="48%" src="https://github.com/user-attachments/assets/8ddc0dc5-8ddd-4d95-9a19-61927f5e7037" alt="Services_2">
  <img width="48%" src="https://github.com/user-attachments/assets/8297607e-e986-46e5-8123-80617e8c45f6" alt="Services_3">
  <img width="48%" src="https://github.com/user-attachments/assets/d2972f92-3ac1-4ad0-938c-0b8a9ad1a50c" alt="Services_4">
  <img width="48%" src="https://github.com/user-attachments/assets/32c09472-7d45-452d-be4e-ee479cef68cb" alt="Services_5">
</div>
</details>

<details>
<summary>🎁 Stocks & Promotions</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" src="https://github.com/user-attachments/assets/2c1019a2-e69d-4410-8a0b-9dd9e1551f71" alt="Stocks_Global">
  <img width="48%" src="https://github.com/user-attachments/assets/84fd6490-05c7-4848-8be5-84166153e25b" alt="Stocks_Germany_Berlin">
  <img width="48%" src="https://github.com/user-attachments/assets/34804411-2058-437c-8767-2fb934974586" alt="Stocks_Germany_Berlin_details">
</div>
</details>

<details>
<summary>💬 Support</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" src="https://github.com/user-attachments/assets/695b4f21-c251-48c5-bb91-c7e5cd421481" alt="Support">
  <img width="48%" src="https://github.com/user-attachments/assets/ffcae780-b527-4697-9ff5-6ee284c3a6fd" alt="Support_2">
  <img width="48%" src="https://github.com/user-attachments/assets/bd0e6bae-8e41-4b80-b2a4-5a6fae0832a8" alt="Support_3">
</div>
</details>

<details>
<summary>👔 Vacancies</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" src="https://github.com/user-attachments/assets/b0cf42fd-ec90-4fd1-aa0b-2d9d76bc1d24" alt="Vacancies_1">
  <img width="48%" src="https://github.com/user-attachments/assets/ef81a976-a804-4024-87e4-c732d81d3a1c" alt="Vacancies">
  <img width="48%" src="https://github.com/user-attachments/assets/9f577934-e42c-45d5-9ee6-b11408cb7ac8" alt="Vacancies_3">
  <img width="48%" src="https://github.com/user-attachments/assets/8af011d8-9f34-4b80-9d22-bb732a1ab1c9" alt="Vacancies_4">
</div>
</details>

<details>
<summary>📰 News</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" src="https://github.com/user-attachments/assets/1b457078-f09f-4646-a8b8-8c51a0bae367" alt="News_Global_details">
</div>
</details>

<details>
<summary>🔐 Authentication</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" src="https://github.com/user-attachments/assets/df7d8e3f-08c9-4f36-9160-82c7c7a5b3bd" alt="Signup">
  <img width="48%" src="https://github.com/user-attachments/assets/92df1cbb-17e1-440e-a976-54a7404fa2f9" alt="Signin">
  <img width="48%" src="https://github.com/user-attachments/assets/f7ac7180-e963-43cd-a307-80ed5f88a45c" alt="Forgot password">
  <img width="48%" src="https://github.com/user-attachments/assets/0c1e92f0-a94f-4ddf-9213-8afad8495139" alt="signout">
</div>
</details>

<details>
<summary>👤 User Cabinet</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" src="https://github.com/user-attachments/assets/bc9362e9-0c8e-4a15-81f9-3dde683cc081" alt="My Cabinet">
  <img width="48%" src="https://github.com/user-attachments/assets/0bb885a8-191d-412d-a6f8-532ca150276e" alt="MyCab">
  <img width="48%" src="https://github.com/user-attachments/assets/d6ad335e-a093-421f-b29b-18e2ba769391" alt="myreq">
  <img width="48%" src="https://github.com/user-attachments/assets/89cb1117-fc4d-43bb-8b68-828fc113fd5c" alt="myreqcancel">
  <img width="48%" src="https://github.com/user-attachments/assets/e14955da-c18f-49c2-8592-3aabcc082ca4" alt="edit_profile">
</div>
</details>

<details>
<summary>💳 Payment Methods</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" src="https://github.com/user-attachments/assets/a803f2c3-7b93-440d-b324-8da3d3927f02" alt="discover">
  <img width="48%" src="https://github.com/user-attachments/assets/05765ee7-a949-402e-9c84-4ffb10de0d32" alt="diners">
  <img width="48%" src="https://github.com/user-attachments/assets/f964aad7-0110-42b2-8add-1a41bfef2b1a" alt="Amex">
  <img width="48%" src="https://github.com/user-attachments/assets/6863d073-d1fb-47ec-b3e3-b50fc26a2e56" alt="visa">
  <img width="48%" src="https://github.com/user-attachments/assets/65989789-f89e-4c55-a53c-42ecbd9ed2a8" alt="jcb">
  <img width="48%" src="https://github.com/user-attachments/assets/2b7bcad3-49e4-43ce-9f41-5c703c1de440" alt="Top_up_mastercard">
  <img width="48%" src="https://github.com/user-attachments/assets/2f717f4b-bc2e-4663-b7d7-f5db9fa77a87" alt="Top_up_union_pay">
  <img width="48%" src="https://github.com/user-attachments/assets/20e30dea-9e54-4f8a-9f7a-3e375c714bfb" alt="Topupmir">
</div>
</details>


## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/astrawilly.git
cd astrawilly
