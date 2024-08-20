#checkov:skip=CKV_DOCKER_2: HEALTHCHECK is not needed for this container
# ----------------------- Base -----------------------
FROM amazon/aws-glue-libs:glue_libs_4.0.0_image_01 AS base

WORKDIR /home/glue_user/workspace

# hadolint ignore=DL3013
RUN pip3 install --disable-pip-version-check --no-compile --no-cache-dir --no-warn-script-location --user --upgrade pip \
  && mkdir -p docker


# ----------------------- Test -----------------------
FROM base AS test

# Install dependencies.
COPY docker/requirements.txt docker/requirements.txt
RUN pip3 install --disable-pip-version-check --no-compile --no-cache-dir --no-warn-script-location --user -r docker/requirements.txt

# Install this package.
COPY src pyproject.toml README.md ./
RUN pip3 install --disable-pip-version-check --no-compile --no-cache-dir --no-warn-script-location --user .


# --------------------- Coverage ---------------------
FROM base AS coverage

# Pass the host user to the container.
ARG USER_ID

# Switch to root to be able to make changes in the container filesystem.
USER root

# Clean up /tmp which may already have glue_user-owned files with the
# old UID.
RUN rm -rf /tmp/* \
  # Change UID of glue_user to be the same as host user. This allows
  # JupyterLab to write to the host system as glue_user.
  && usermod -u $USER_ID glue_user

# Switch to glue_user to be able to make changes for the user itself.
USER glue_user

# Install dependencies.
COPY docker/requirements.txt docker/requirements.txt
RUN pip3 install --disable-pip-version-check --no-compile --no-cache-dir --no-warn-script-location --user -r docker/requirements.txt

# Install this package.
COPY src pyproject.toml README.md ./
RUN pip3 install --disable-pip-version-check --no-compile --no-cache-dir --no-warn-script-location --user . \
  # Prepare a /tmp directory needed by Spark to start.
  && mkdir -p /tmp/spark-events
