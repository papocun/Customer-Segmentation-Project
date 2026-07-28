# ☁️ How to Deploy & Open Your App Live on AWS

This guide provides step-by-step instructions to host your **Customer Segmentation Web App** (Streamlit Frontend + FastAPI Backend) on **Amazon Web Services (AWS)** so anyone can access it directly from a browser URL.

---

## 🎯 Recommended Deployment Option: AWS EC2 (Free Tier)

Using an **AWS EC2 Virtual Server** with Docker Compose is the simplest, most reliable way to run both your frontend (Streamlit) and backend (FastAPI) together.

---

### 📋 Step-by-Step Guide: Deploying on AWS EC2

#### Step 1: Log in to AWS Console
1. Go to [https://aws.amazon.com/console/](https://aws.amazon.com/console/) and sign in.
2. In the top search bar, search for **EC2** and select **EC2 Virtual Servers in the Cloud**.

---

#### Step 2: Launch a New EC2 Instance
1. Click the orange **"Launch instance"** button.
2. **Name**: Enter `customer-segmentation-app`.
3. **Application and OS Image (AMI)**: Select **Ubuntu** (Ubuntu Server 22.04 LTS or 24.04 LTS).
4. **Instance Type**: Select **`t2.micro`** or **`t3.micro`** *(Free tier eligible)*.
5. **Key Pair**: Select an existing key pair, or click **Create new key pair** (e.g., `my-aws-key.pem`) and download it.

---

#### Step 3: Configure Network & Security Group (CRITICAL)
Under **Network settings**, click **Edit** and set up the following Inbound Security Group Rules so the website ports are publicly reachable:

| Rule Type | Port Range | Source Type | Description |
| :--- | :--- | :--- | :--- |
| **SSH** | `22` | My IP / Anywhere | SSH Access for terminal |
| **Custom TCP** | `8501` | Anywhere (`0.0.0.0/0`) | **Streamlit Web UI** |
| **Custom TCP** | `8000` | Anywhere (`0.0.0.0/0`) | **FastAPI Backend API** |

> ⚠️ **Important**: Opening port `8501` allows your browser to open the Streamlit web interface directly!

---

#### Step 4: Automated Setup via User Data (Optional / Automated)
Scroll down to **Advanced details**, expand it, scroll to the **User data** text box at the very bottom, and paste this script:

```bash
#!/bin/bash
curl -fsSL https://raw.githubusercontent.com/papocun/Customer-Segmentation-Project/main/scripts/deploy_aws_ec2.sh | bash
```

*This automatically installs Docker, clones your GitHub repository, builds the containers, and launches the app when the server boots!*

---

#### Step 5: Launch & Access Your Web App!
1. Click **"Launch Instance"**.
2. Go back to the **EC2 Instances list** and click on your running instance.
3. Copy your **Public IPv4 address** (e.g., `54.210.12.34`).
4. Open your web browser and navigate to:
   ```text
   http://<YOUR-EC2-PUBLIC-IP>:8501
   ```
   *Example: `http://54.210.12.34:8501`*

🎉 **Your app is now live on the internet!**

---

## ⚡ Method 2: AWS Elastic Beanstalk (Managed Deployment)

If you prefer managed AWS infrastructure:
1. Search for **Elastic Beanstalk** in the AWS Console.
2. Click **Create Application**.
3. Select Platform: **Docker** (Docker running on 64bit Amazon Linux 2023).
4. Under Application code, upload your repository's `docker-compose.yml` or `Dockerrun.aws.json`.
5. Click **Create environment**. Elastic Beanstalk will automatically assign you a `.elasticbeanstalk.com` domain URL.

---

## 🌟 Alternative: Free 1-Click Hosting Options

If you want a free & quick option without setting up AWS credit cards:
- **Streamlit Community Cloud**: Connect your GitHub account at [share.streamlit.io](https://share.streamlit.io), select `papocun/Customer-Segmentation-Project`, set main file as `Homepage.py`, and click Deploy!
- **Render.com**: Deploy directly as a Web Service using your `Dockerfile` or `docker-compose.yml`.

---

## 🛠️ Managing Your App on AWS EC2

To SSH into your EC2 instance from your terminal:
```bash
ssh -i "my-aws-key.pem" ubuntu@<YOUR-EC2-PUBLIC-IP>
```

Check running app containers:
```bash
sudo docker compose ps
```

View live logs:
```bash
sudo docker compose logs -f
```

Restart application:
```bash
sudo docker compose restart
```
