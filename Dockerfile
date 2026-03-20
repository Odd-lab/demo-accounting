FROM odoo:18.0

USER root

# Install production dependencies
ADD requirements.txt /mnt/requirements.txt
RUN pip3 install --no-cache-dir --ignore-requires-python --break-system-packages --ignore-installed -r /mnt/requirements.txt

RUN apt-get update && apt-get install -y \
    fonts-thai-tlwg \
    fonts-noto-cjk \
    fontconfig \
    && fc-cache -fv \
    && rm -rf /var/lib/apt/lists/*

USER odoo

# Setup Odoo
ADD --chown=odoo:odoo addons /mnt/addons
ADD --chown=odoo:odoo odoo.conf /etc/odoo/odoo.conf
