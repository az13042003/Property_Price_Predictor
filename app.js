function getBathValue() {
  const uiBathrooms = document.getElementsByName("uiBathrooms");
  for (let i = 0; i < uiBathrooms.length; i++) {
    if (uiBathrooms[i].checked) {
      return parseInt(uiBathrooms[i].value);
    }
  }
  return -1; // Invalid Value
}

function getBHKValue() {
  const uiBHK = document.getElementsByName("uiBHK");
  for (let i = 0; i < uiBHK.length; i++) {
    if (uiBHK[i].checked) {
      return parseInt(uiBHK[i].value);
    }
  }
  return -1; // Invalid Value
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  const sqft = document.getElementById("uiSqft");
  const bhk = getBHKValue();
  const bathrooms = getBathValue();
  const location = document.getElementById("uiLocations");
  const estPrice = document.getElementById("uiEstimatedPrice");

  const url = "http://127.0.0.1:5000/predict_home_price"; // Use this if you are NOT using nginx

  $.post(url, {
    total_sqft: parseFloat(sqft.value),
    bhk: bhk,
    bath: bathrooms,
    location: location.value
  }, function (data, status) {
    if (status === 'success') {
      console.log(data.estimated_price);
      estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
    } else {
      console.error("Error:", status);
      estPrice.innerHTML = "<h2>Error estimating price</h2>";
    }
  }).fail(function (xhr, status, error) {
    console.error("Error:", status, error);
    estPrice.innerHTML = "<h2>Error estimating price</h2>";
  });
}

function onPageLoad() {
  console.log("document loaded");
  const url = "http://127.0.0.1:5000/get_location_names"; // Use this if you are NOT using nginx

  $.get(url, function (data, status) {
    if (status === 'success') {
      console.log("got response for get_location_names request");
      if (data) {
        const locations = data.locations;
        const uiLocations = document.getElementById("uiLocations");
        $('#uiLocations').empty();
        locations.forEach(function (location) {
          const opt = new Option(location);
          $('#uiLocations').append(opt);
        });
      }
    } else {
      console.error("Error:", status);
    }
  }).fail(function (xhr, status, error) {
    console.error("Error:", status, error);
  });
}

window.onload = onPageLoad;
