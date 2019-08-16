from noaa_radar import radar

noaa = radar.Radar()

image = noaa.get_base_reflectivity('HTX')
image.save("base_reflectivity.jpg")