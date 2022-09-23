
      function getColorFor(str) {
        // java String#hashCode
        var hash = 0;
        for (var i = 0; i < str.length; i++) {
          hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        var red = (hash >> 24) & 0xff;
        var grn = (hash >> 16) & 0xff;
        var blu = (hash >> 8) & 0xff;
        return "rgb(" + red + "," + grn + "," + blu + ")";
      }
      var osmUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
      var osmAttrib =
        '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors';
      var osm = L.tileLayer(osmUrl, { maxZoom: 18, attribution: osmAttrib });
      var map = L.map("map2", {
        layers: [osm],
        center: new L.LatLng(0, 0),
        zoom: 2,
      });
      var timeline;
      var timelineControl;

      function onLoadData(data) {
        timeline = L.timeline(data, {
          style: function (data) {
            return {
              stroke: false,
              color: getColorFor(data.properties.name),
              fillOpacity: 0.5,
            };
          },
          waitToUpdateMap: true,
          onEachFeature: function (feature, layer) {
            layer.bindTooltip(feature.properties.name);
          },
        });

        timelineControl = L.timelineSliderControl({
          formatOutput: function (date) {
            return new Date(date).toLocaleDateString();
          },
          enableKeyboardControls: true,
        });
        timeline.addTo(map);
        timelineControl.addTo(map);
        timelineControl.addTimelines(timeline);
      }
