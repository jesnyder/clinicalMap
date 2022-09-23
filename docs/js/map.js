
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

				/*
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

			*/

			function onEachFeature(feature, layer) {
					layer.on({
						mouseover: highlightFeature,
						mouseout: resetHighlight,
						click: zoomToFeature
					});
				}


			function trialStyle (feature) {
					return feature.properties && feature.properties.style;
				}

			function onEachTrial(feature, layer) {
				var aff = feature.properties.aff;
				var url = feature.properties.url;
				var name = feature.properties.name;

					var popupContent = '<p><b>'
						 + feature.properties.name
						 + '</b><br>'
						 + feature.properties.aff
						 + '<br>'
						 + 'Enrolled: ' + feature.properties.enrolled
						 + '<br>'
						 + '<a href="' + feature.properties.url + '" target="_blank" rel="noopener">'
						 + feature.properties.url + '</a>'
						 + '</p>';

						if (feature.properties && feature.properties.popupContent) {
								popupContent += feature.properties.popupContent;
							}
							layer.bindPopup(popupContent);
						}

			function trialToLayer(feature, latlng) {
				//map.createPane("locationMarker");
				//map.getPane("locationMarker").style.zIndex = 999;
				return L.circleMarker(latlng, {
					radius: feature.properties.radius,
					opacity: feature.properties.opacity,
					fillOpacity: feature.properties.fillOpacity,
					fillColor: feature.properties.fillColor,
					color: feature.properties.color,
					weight: 1,
					//pane: feature.properties.zindex ,
				});
			}


			/*
			var geojson_all = L.geoJson(groupall, {
				style: trialStyle,
				onEachFeature: onEachTrial,
				pointToLayer: trialToLayer,
			}).addTo(map).addTo(trialall);


			var geojson_undeclared = L.geoJson(groupboth, {
				style: trialStyle,
				onEachFeature: onEachTrial,
				pointToLayer: trialToLayer,
			}).addTo(map);

*/
var slider = L.timelineSliderControl({
		formatOutput: function (date) {
			return moment(date).format("YYYY-MM-DD");
		},
	});
	map.addControl(slider);

var pointersUndeclared = L.timeline(groupundeclared, {
		style: trialStyle,
		onEachFeature: onEachTrial,
		pointToLayer: trialToLayer,
		}).addTo(map);

var pointersAllo = L.timeline(groupallo, {
	style: trialStyle,
	onEachFeature: onEachTrial,
	pointToLayer: trialToLayer,
	}).addTo(map);

var pointersAuto = L.timeline(groupauto, {
		style: trialStyle,
		onEachFeature: onEachTrial,
		pointToLayer: trialToLayer,
		}).addTo(map);

var pointersBoth = L.timeline(groupboth, {
		style: trialStyle,
		onEachFeature: onEachTrial,
		pointToLayer: trialToLayer,
		}).addTo(map);

slider.addTimelines(pointersUndeclared, pointersAllo, pointersAuto, pointersBoth);
