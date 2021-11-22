for var in "$@"
do
  case "$var" in
    run)
      flask run
      ;;
    docker-build)
      docker build --tag api-users:latest .
      ;;
    docker-run)
      docker run --name api-users -p 5000:5000 --rm api-users:latest
      ;;
    docker-rm)
      docker stop api-users && docker rm api-users
      ;;
    rbr)
      bash ./run.sh docker-rm docker-build docker-run
      ;;
    *)
      ;;
  esac
done
