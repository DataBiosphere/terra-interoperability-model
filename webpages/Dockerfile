FROM httpd:2.4

COPY ./www/ /usr/local/apache2/htdocs/
COPY ./httpd-container.conf /usr/local/apache2/conf/httpd.conf

COPY ./TerraCoreDataModel.html /usr/local/apache2/htdocs/TerraCoreDataModel.html
COPY ./TerraCoreValueSets/TerraCoreValueSets.html /usr/local/apache2/htdocs/TerraCoreValueSets/TerraCoreValueSets.html
COPY ./TerraDCAT_ap/TerraDCAT_ap.html /usr/local/apache2/htdocs/TerraDCAT_ap/TerraDCAT_ap.html