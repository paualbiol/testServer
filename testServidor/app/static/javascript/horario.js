
//EMPIEZA EL HORARIO
 var timeSets = [];

    $(function () {
        var isMouseDown = false;
        $("#timeTable td")
                .mousedown(function () {
                    isMouseDown = true;
                    $(this).toggleClass("highlighted");                  
                    return false; 
                })
                .mouseover(function () {
                    if (isMouseDown) {
                        $(this).toggleClass("highlighted");                        
                    }
                });
        $(document).mouseup(function () {
                    isMouseDown = false;
                });
        $('#btn-save-TS').on('click', function () {
            saveTimeSave();
        });        
    });
    
    var saveTimeSave = function () {
        for (i = 1; i < 8; i++) {
            for (j = 0; j < 24; j++) {
                if ($("#" + i + "" + j).css("backgroundColor") == "rgb(135, 206, 235)") {
                    if (timeSets.indexOf(i + "" + j) == -1) {
                        timeSets.push(i + "" + j);
                    }
                }else{
                    realIndex = timeSets.indexOf(i + "" + j);
                    if (realIndex != -1) {
                        timeSets.splice(realIndex, 1);
                    }
                }
            }
        }
        console.log(timeSets.valueOf());    
    };

function check(id)
  {
    if(mouseDown)
      {
        document.getElementById(id).checked = 1-document.getElementById(id).checked;
        // document.getElementById(id).checked = true;
        // ^ If you only want to turn them on, use this.
      }
  }
 
  var mouseDown = 0;
  document.body.onmousedown = function()
  {
    ++mouseDown;
  }
 
  document.body.onmouseup = function()
  {
  --mouseDown;
  }
