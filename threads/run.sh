for var in "$@"
do
  case "$var" in
    run)
      flask run
      ;;
    docker-build)
      docker build --tag api-threads:latest .
      ;;
    docker-run)
      docker run --name api-threads -p 5000:5000 --rm api-threads:latest
      ;;
    docker-rm)
      docker stop api-threads && docker rm api-threads
      ;;
    rbr)
      bash ./run.sh docker-rm docker-build docker-run
      ;;
    *)
      ;;
  esac
done
