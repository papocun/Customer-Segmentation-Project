# Customer Segmentation Project (End-to-End)

An end-to-end Machine Learning web application for customer segmentation utilizing **FastAPI** for the model prediction backend and **Streamlit** for the interactive frontend UI. Fully containerized with **Docker** and **Docker Compose**.

---

## 🚀 Quick Start (Local Docker)

To run the application locally using Docker:

```bash
docker-compose up --build
```

Access the services in your browser:
- **Streamlit Web UI**: [http://localhost:8501](http://localhost:8501)
- **FastAPI Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ☁️ Deployment to AWS (Host Live on the Web)

To deploy this application to AWS so you can open it directly from a web URL, refer to our detailed step-by-step guide:

👉 **[AWS Deployment Guide (AWS_DEPLOYMENT.md)](AWS_DEPLOYMENT.md)**

Includes:
- Launching AWS EC2 instance (Free Tier)
- Setting up Security Groups & Ports (`8501` & `8000`)
- Automated EC2 launch script (`scripts/deploy_aws_ec2.sh`)
- AWS Elastic Beanstalk configuration (`Dockerrun.aws.json`)
