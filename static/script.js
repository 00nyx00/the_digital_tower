/* DELETE THE COMMENT MARKS BEFORE UPLOAD!!!!
// on load check if yarn was collected
if (localStorage.getItem('yarn_collected') === 'true') {
    // If we found it before, hide it immediately
    const yarnElement = document.querySelector('.scoreable[data-value="yarn"]');
    if (yarnElement) yarnElement.style.display = 'none';
}

// on load check if cable was collected
if (localStorage.getItem('cable_collected') === 'true') {
    // If we found it before, hide it immediately
    const cableElement = document.querySelector('.scoreable[data-value="cable"]');
    if (cableElement) cableElement.style.display = 'none';
}
    

// on load check if bed was clicked
if (localStorage.getItem('bed_clicked') === 'true') {
  const bedElement = document.querySelector('.scoreable[data-value="bed"]');
  if (bedElement) {
      // Apply the "disabled" look immediately
      bedElement.style.pointerEvents = 'none';
      bedElement.style.cursor = 'default';
      bedElement.style.opacity = '0.7';
  }
}
*/

// send values of clicked items

let bedTimerInterval; // Store timer ID globally
// Setup variables for the Plant popup
const plantPopup = document.getElementById('planterror');
let plantFadeTimer;


document.querySelectorAll('.scoreable').forEach(element => {
    element.addEventListener('click', function(e) {
        //  Get the value (e.g., 'test_good' or 'test_bad')
        let val = this.getAttribute('data-value');

        // Send it to your /save route
        fetch('/save', {
            method: 'POST',
            body: new URLSearchParams({'value': val}),
            // still sends the request if the page changes, so can link can also be scoreable
            keepalive: true
        });
        
        if (val === 'yarn') {
          // Hide the element
          this.style.display = 'none'; 

          // remember it was found
            localStorage.setItem('yarn_collected', 'true');
          
          // Show the custom alert overlay
            const overlay = document.getElementById('yarn-alert');
            if (overlay) {
                overlay.style.display = 'flex'; // 'flex' enables the centering from CSS
            }
        }

        if (val === 'cable') {
            // Hide the element
            this.style.display = 'none'; 
  
            // remember it was found
              localStorage.setItem('cable_collected', 'true');
            
            // Show the custom alert overlay
              const overlay = document.getElementById('cable-alert');
              if (overlay) {
                  overlay.style.display = 'flex'; // 'flex' enables the centering from CSS
              }
          }

        
    // --- BED LOGIC ---
    if (val === 'bed') {
        
        this.style.pointerEvents = 'none'; // Makes it unclickable
        this.style.cursor = 'default';     // Changes cursor back to arrow
        this.style.opacity = '0.7';        // Dims the bed to show it is "done"

        // remember it was clicked
        localStorage.setItem('bed_clicked', 'true');

        // POPUP LOGIC
        const overlay = document.getElementById('bed-overlay');
        const timerText = document.getElementById('timer-count');
        
        // Reset timer
        clearInterval(bedTimerInterval);
        let timeLeft = 10;
        timerText.innerText = timeLeft;
        
        // Show overlay
        overlay.style.display = 'flex';
        
        // Start Countdown 
        bedTimerInterval = setInterval(function(){
          timeLeft--; 
          timerText.innerText = timeLeft;

          if(timeLeft <= 0){
              clearInterval(bedTimerInterval);
              overlay.style.display = 'none';
          } 
      }, 1000);
    }
      
    // ---Plant Logic ---
    if (val === 'plant') {
        // Show the popup
        if (plantPopup) {
            plantPopup.classList.add('show');

            // Reset timer if clicked again rapidly
            clearTimeout(plantFadeTimer);

            // Hide after 3 seconds
            plantFadeTimer = setTimeout(() => {
                plantPopup.classList.remove('show');
            }, 3000);
        }
    }

    //restart logic
    if (val === 'restart') {
        window.location.href = '/';
        return;
      }


    // ---Sparkle Logic ---
    const sparkle = this.querySelector('.sparkle');

        if (sparkle) {
            sparkle.style.position = 'fixed'; 

            //  Set the position to the mouse coordinates
            sparkle.style.left = e.clientX + 'px';
            sparkle.style.top = e.clientY + 'px';

            sparkle.classList.add('show');

            // Hide after time
            setTimeout(() => {
                sparkle.classList.remove('show');
            }, 2000);
        }

    });
});

// close the yarn alert
const closeAlertBtn = document.getElementById('close-alert');
if (closeAlertBtn) {
    closeAlertBtn.addEventListener('click', function() {
        document.getElementById('yarn-alert').style.display = 'none';
    });
}
// close the cable alert
const closeAlertBtnCable = document.getElementById('close-alert-cable');
if (closeAlertBtnCable) {
    closeAlertBtnCable.addEventListener('click', function() {
        document.getElementById('cable-alert').style.display = 'none';
    });
}
// close bed alert
const closeBedBtn = document.getElementById('close-bed-btn');
if (closeBedBtn) {
    closeBedBtn.addEventListener('click', function() {
        document.getElementById('bed-overlay').style.display = 'none';
        clearInterval(bedTimerInterval);
    });
}




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


//draggable computer window

const dragger = document.querySelector(".window-container");
const handle = document.querySelector(".window-header");

let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

handle.onmousedown = dragMouseDown;

function dragMouseDown(e) {
    e.preventDefault();
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    document.onmousemove = elementDrag;
}

function elementDrag(e) {
    e.preventDefault();
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    dragger.style.top = (dragger.offsetTop - pos2) + "px";
    dragger.style.left = (dragger.offsetLeft - pos1) + "px";
}

function closeDragElement() {
    document.onmouseup = null;
    document.onmousemove = null;
}

