// send values of clicked items

document.querySelectorAll('.scoreable').forEach(element => {
    element.addEventListener('click', function() {
        // 1. Get the value (e.g., 'test_good' or 'test_bad')
        let val = this.getAttribute('data-value');

        // 2. Send it to your /save route
        fetch('/save', {
            method: 'POST',
            body: new URLSearchParams({'value': val}),
            // still sends the request if the page changes, so can link can also be scoreable
            keepalive: true
        });
        
        // No .then() block means the UI remains exactly as it is.
    });
});



// prevent dragging images

document.querySelectorAll('img').forEach(img => {
    img.setAttribute('draggable', 'false');
});



//marquee source https://codepen.io/pprakash/pen/oNxNeQE

function Marquee(selector, speed) {
    const parentSelector = document.querySelector(selector);
    const clone = parentSelector.innerHTML;
    const firstElement = parentSelector.children[0];
    let i = 0;
    console.log(firstElement);
    parentSelector.insertAdjacentHTML('beforeend', clone);
    parentSelector.insertAdjacentHTML('beforeend', clone);
    parentSelector.insertAdjacentHTML('beforeend', clone);
    parentSelector.insertAdjacentHTML('beforeend', clone);
    parentSelector.insertAdjacentHTML('beforeend', clone);
    parentSelector.insertAdjacentHTML('beforeend', clone);
    parentSelector.insertAdjacentHTML('beforeend', clone);
    parentSelector.insertAdjacentHTML('beforeend', clone);
  
  
    setInterval(function () {
      firstElement.style.marginLeft = `-${i}px`;
      if (i > firstElement.clientWidth) {
        i = 0;
      }
      i = i + speed;
    }, 0);
  }
  
  //after window is completed load
  //1 class selector for marquee
  //2 marquee speed 0.2
  window.addEventListener('load', Marquee('.marquee', 0.2))


//mouse trail source https://github.com/tholman/cursor-effects

window.addEventListener("load", (event) => {
    new cursoreffects.ghostCursor(
      {image: '/static/img/pinkcursorresize.png'}
    );
  });  