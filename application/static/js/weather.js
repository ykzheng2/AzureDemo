if (navigator.geolocation) {
  //Return the user's longitude and latitude on page load using HTML5 geolocation API
  window.onload = function() {
    navigator.geolocation.getCurrentPosition(getCurrentLocation);
  };
}

function getCurrentLocation(position) {
  latitude = position.coords.latitude;
  longitude = position.coords.longitude;

  console.log(latitude);
  console.log(longitude);

  $.getJSON(
    "https://api.openweathermap.org/data/2.5/weather?lat=" +
      latitude +
      "&lon=" +
      longitude +
      "&APPID=3d77d9cca2476d1692dedc4991038747&units=imperial",
    function(data) 
    {
      console.log(data);
      //console.log(weather.main.temp);
      $(".city")[0].append(data.name + " ");
      $(".temperature")[0].append(((data.main.temp-32)*(5/9)).toFixed(1)+ "°C");
      $(".humidity")[0].append(data.main.humidity + "% Humidity");
      $(".weatherdescription")[0].append(data.weather[0].description + " ");
    }
  );
}
