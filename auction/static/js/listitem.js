let id_expiration_time = document.getElementById(
  'id_expiration_time'
);
let id_location = document.getElementById('id_location');
let datetimealert = document.getElementById('datetime-alert');
let datetimepicker = new SimplePicker();

id_location.readOnly = true;
id_expiration_time.readOnly = true;
id_location.placeholder = 'Fetching data...';

id_expiration_time.addEventListener('click', (e) => {
  datetimepicker.open();
});

datetimepicker.on('submit', (date, readableDate) => {
  console.log(date.toUTCString());
  let now = new Date();
  if (date < now.setHours(now.getHours() + 1)) {
    datetimepicker.reset();
    id_expiration_time.value = '';
    datetimealert.style = 'display:block;';
    return;
  } else {
    datetimealert.style = 'display:none;';
  }
  let timezone = new Date()
    .toString()
    .match(/([A-Z]+[\+-][0-9]+)/)[1];
  let s = date.toUTCString();
  let pre = s.slice(0, s.lastIndexOf(':'));
  id_expiration_time.value = pre + ' ' + timezone;
});

async function postData(url = '', data = {}) {
  const response = await fetch(url, {
    method: 'GET',
    mode: 'cors',
    cache: 'no-cache',
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
  });
  return response.json();
}

postData('https://json.geoiplookup.io/', {}).then((data) => {
  console.log(data);
  if (!data) {
    return;
  }

  let postalCode = data.postal_code ? data.postal_code + ' ' : '';
  let city = data.city ? data.city + ', ' : '';
  let country = data.country_name ? data.country_name : '';
  let locationString = `${postalCode}${city}${country}`;

  /* Uncomment the line below for XSS. The line simulates
  a dangerous response coming from the API. */
  // locationString = '<div onmouseover="alert(\'xss\');" style="width:10000px; height:10000px;"></div>';

  /* Uncomment the lines below to prevent XSS. The regular
  expression rejects any non-alphabetic letters, which
  prevents any dangerous characters, such as <, “, or /, 
  from being inserted into the HTML DOM. The solution is
  incomplete, as it also prevents some legitimate characters
  from being used. */
  // if(!locationString.match(/^[0-9a-zA-Z]+$/)){
  //   console.log('XSS may have been attempted');
  //   return;
  // }

  let newNode = document.createElement('div');
  /* The line below demonstrates an XSS vulnerability. 
  The vulnerability in question can be easily exploited by
  the providers of the geolocation API (including any
  attackers who may have compromised the service). One way
  to do this would be by returning a HTML element that has
  JavaScript code as a value of its “mouseover” attribute
  (instead of returning the city/country data). The
  JavaScript code would then be executed in the application,
  and it could be used, for example, to steal session keys
  or to trick users for their passwords (e.g., by providing
  a fake login form). (FLAW 1) */
  newNode.innerHTML = `<div id="notification">Your location (${locationString}) has been automatically filled using your IP address. Click <a id="enable-edit">here</a> if this is incorrect.</div><br />`;
  id_location.parentNode.insertBefore(
    newNode,
    id_location.nextSibling
  );

  let enableEdit = document.getElementById('enable-edit');
  enableEdit.addEventListener('click', (e) => {
    id_location.readOnly = false;
    notification.style = 'display:none;';
  });

  id_location.value = locationString;
});
