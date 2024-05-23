# ----------------------- Base -----------------------
FROM amazon/aws-glue-libs:glue_libs_4.0.0_image_01 as base

# Copy requirements file that contains tooling.
WORKDIR /home/glue_user/workspace
COPY docker/requirements.txt ./

RUN pip3 install --no-cache-dir --no-warn-script-location --user --upgrade pip==24.0 \
  # Install dev requirements.
  && pip3 install --no-cache-dir --no-warn-script-location --user -r requirements.txt


# ----------------------- Test -----------------------
FROM base as test

COPY src pyproject.toml README.md ./

# Install this package.
RUN pip3 install --no-cache-dir --no-warn-script-location --user .


# --------------------- Coverage ---------------------
FROM base as coverage

# Pass the host user to the container.
ARG USER_ID

# Switch to root to be able to make changes in the container filesystem.
USER root

# Change UID of glue_user to be the same as host user. This allows
# JupyterLab to write to the host system as glue_user.
RUN usermod -u "$USER_ID" glue_user \
  # Clean up /tmp which may already have glue_user-owned files with the
  # old UID.
  && rm -rf /tmp/*

# Switch to glue_user to be able to make changes for the user itself.
USER glue_user

COPY src pyproject.toml README.md ./

# Install this package.
RUN pip3 install --no-cache-dir --no-warn-script-location --user . \
  # Prepare a /tmp directory needed by Spark to start.
  && mkdir -p /tmp/spark-events
