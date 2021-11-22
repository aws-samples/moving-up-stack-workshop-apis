for var in "$@"
do
  case "$var" in
    run)
      flask run
      ;;
    docker-build)
      docker build --tag api-posts:latest .
      ;;
    docker-run)
      docker run --name api-posts -p 5000:5000 --rm api-posts:latest
      ;;
    docker-rm)
      docker stop api-posts && docker rm api-posts
      ;;
    rbr)
      bash ./run.sh docker-rm docker-build docker-run
      ;;
    *)
      ;;
  esac
done
