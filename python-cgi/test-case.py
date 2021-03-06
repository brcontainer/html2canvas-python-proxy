#!C:\\Python27\\python.exe

print "Content-Type: text/html\r\n"
print """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>html2canvas python proxy</title>
        <script src="http://cdnjs.cloudflare.com/ajax/libs/html2canvas/0.4.1/html2canvas.min.js"></script>
        <style>
            #box {
                width: 410px;
                background: #c0c0c0;
            }
            #box p {
                padding: 5px;
            }
        </style>
        <script>
        //<![CDATA[
        (function() {
            window.onload = function(){
                html2canvas(document.body, {
                    "logging": true, //Enable log (use Web Console for get Errors and Warnings)
                    "proxy":"proxy.py",
                    "onrendered": function(canvas) {
                        var img = new Image();
                        img.onload = function() {
                            img.onload = null;
                            document.body.appendChild(img);
                        };
                        img.onerror = function() {
                            img.onerror = null;
                            if(window.console.log) {
                                window.console.log("Not loaded image from canvas.toDataURL");
                            } else {
                                alert("Not loaded image from canvas.toDataURL");
                            }
                        };
                        img.src = canvas.toDataURL("image/png");
                    }
                });
            };
        })();
        //]]>
        </script>
    </head>
    <body>
        <div id="box">
            <p>
                <img alt="google maps static" src="http://maps.googleapis.com/maps/api/staticmap?center=40.714728,-73.998672&amp;zoom=12&amp;size=400x300&amp;maptype=roadmap&amp;sensor=false">
                <br>
                <img alt="facebook image redirect" src="https://graph.facebook.com/100007213599954/picture">
                <br>
                <img alt="bmp test" src="http://caio.ueberalles.net/img.old/modules/imagemagick/data/test.bmp">
            </p>
        </div>
    </body>
</html>
"""
