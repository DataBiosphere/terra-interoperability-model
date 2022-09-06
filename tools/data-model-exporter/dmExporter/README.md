### SET UP
Navigate to docker subdirectory, build the image:
```sh
cd tools/data-model-exporter/dmExporter  # Navigate to the dmExporter directory, where our Dockerfile is
docker build -t dm-exporter .
```

Check for the image, get IMAGE ID:
```sh
docker images
image_id="<IMAGE_ID>"
image_id=ea804e8187ef
```

Get path to Data Models, store to variable:
source="/Users/qhoque/GIT/terra-interoperability-model/src/terra-core"


### RUN THE SCRIPT
docker run -it --mount type=bind,source=$source,target="/source" <IMAGE_ID> -f "<Data Model File>" -l <Class_List>

```sh
docker run -it --mount type=bind,source=$source,target="/source" $image_id -f "/source/TerraDCAT-AP.ttl" -l DataCollection
```

### Troubleshooting
