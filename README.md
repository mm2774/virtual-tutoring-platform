# virtual-tutoring-platform

HackOurCampus Virtual Tutoring App

1. Start Docker/Docker Desktop
2. Create .env.dev inside app directory following .env.example
3. Run "docker-compose up -d --build"
4. Run any python manage.py ... commands in docker by "docker-compose exec sessions python manage.py ..."
5. To remove the docker container/volumes, run "docker-compose down -v"
