# Trip Planner

Trip Planner app is a convenient way to plan your future trips and document your past trips. 
Among others, a signed user can:
* create, view, update and delete trips with specified dates and descriptions,
* add notes and specify activities for each day of the trip,
* view your trips and daily activities on a calendar,
* create, view, update and delete trips with specified dates and descriptions,
* upload photos for each trip (current app version supports 1 photo per trip).

You can see the live version of the app at [Trip Planner](https://trip-planner-website.herokuapp.com "Trip Planner").

You can also install the app locally, following the below instructions.
## Setup

You will need Docker installed to run app locally. 
To install Docker, follow instructions on [official Docker documentation](https://docs.docker.com/get-docker/ "Docker Documentation").

When you have Docker installed, follow these steps:


1. Clone the project:

```bash
  git clone https://github.com/ankurahuja-tech/trip-planner.git
```

2. Go to the project directory:

```bash
  cd trip-planner
```

3. Create local .env file:

```bash
  cp ./.env.example.dev ./.env
```

4. Build docker image and run docker containers (web and db) in detached mode:

```bash
  docker-compose up -d --build
```

5. Finally navigate to http://127.0.0.1:8000/ in your browser and verify that the app is running.

6. After finishing using the app, stop and remove containers: 

```bash
docker-compose down -v
```

### Running tests:

To run tests, run the following command while the docker containers are running:

```bash
docker-compose exec web pytest -v --ds=config.settings.test
```

### Basic troubleshooting:

If the app isn't working after running the docker containers (see step 4), verify that the containers (web and db) are in fact running:

```bash
  docker ps
```

If the containers are running, verify that the Django app within the container is running:

```bash
  docker-compose logs -f
```
## Technologies

Project is created mainly with:
* Python 3.10,
* Poetry,
* Django with Django REST Framework,
* Pytest with pytest-django,
* PostgreSQL with PostGIS,
* Docker,
* HTML5 / CSS3 / Bootstrap 5,
* Leaflet.js,
* FullCalendar.

Production technologies and hosting providers:
* Gunicorn,
* WhiteNoise,
* AWS S3 Bucket with django-storages,
* Heroku.
## Authors

[@ankurahuja-tech](https://www.github.com/ankurahuja-tech)

  
## License

[MIT](https://choosealicense.com/licenses/mit/)