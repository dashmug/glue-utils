FROM amazon/aws-glue-libs:glue_libs_4.0.0_image_01

# Copy requirements file that contains tooling.
WORKDIR /home/glue_user/workspace
COPY . ./

RUN pip3 install --no-cache-dir --no-warn-script-location --user --upgrade pip==24.0 \
  # Install dev requirements.
  && pip3 install --no-cache-dir --no-warn-script-location --user -r requirements.txt  \
  # Install this package.
  && pip3 install --no-cache-dir --no-warn-script-location --user . \
  # Prepare a /tmp directory needed by Spark to start.
  && mkdir -p /tmp/spark-events
