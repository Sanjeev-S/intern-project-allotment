$(document).ready(function () {


   /* $.get("http://10.32.58.130:5000/manager/M1",{},function (data) {
        console.log("get call")
        console.log(data)
    });*/



    $.get("/user", {}, function (ManagerName) {
        Get(ManagerName);
        (function poll() {
            setTimeout(function () {
                Get(ManagerName);
                poll();
            }, 1000)
        })();

    });

    function Get(ManagerName){
       // $.get("http://10.32.58.130:5000/manager/"+ManagerName,{},function (Projects) {
          $.get("http://localhost:5000/manager/"+ManagerName,{},function (Projects) {
            $("#dynamic_div").remove();
            var dynamicdiv = $("<div id=\"dynamic_div\">");

            $.each(Projects, function(ProjectName, ProjectStruct){
                var P1 = $("<h6>");
                P1.text(ProjectName);
                dynamicdiv.append(P1);
                var form=$("<form>");

                // if ProjectStruct.fixed is true add a class to the student and dont add select button

                if (!ProjectStruct.fixed) {
                    for (var i = 0; i < ProjectStruct.students.length; i++) {
                        /*var input = $("<input>");
                        input.attr("type", "radio");
                        input.attr("name", ProjectName);
                        input.attr("value", ProjectStruct.students[i]);
                        form.append(input)*/
                        var student = $("<a>");
                        //student.attr("href", "/static/" + ProjectStruct.students[i] + ".pdf")
                        //student.attr("target", "=\"_blank\"")
                        student.text(ProjectStruct.students[i])
                        form.append(student);


                        form.append("&nbsp;");
                        form.append("&nbsp;");

                        var resumelink = $("<a>");
                        resumelink.attr("href","/static/" + ProjectStruct.students[i] + ".pdf")
                        resumelink.attr("target", "=\"_blank\"")

                        var input1 = $("<input>");
                        input1.attr("type", "button");
                        input1.attr("value", "Resume");
                        input1.addClass("resume-class")
                        //input1.attr("href", "/static/" + ProjectStruct.students[i] + ".pdf")
                        resumelink.append(input1)
                        form.append(resumelink)

                        form.append("&nbsp;");
                        form.append("&nbsp;");

                        var input = $("<input>");
                        input.attr("type", "button");
                        input.attr("name",ProjectStruct.students[i]);
                        input.attr("value", "select");
                        input.addClass("submit")
                      //  input.addClass("btn btn-default")
                        input.attr("id",ProjectName);
                        input.text("Select")
                        form.append(input)



                        /*var button = $("<button>");
                        dynamicdiv.append(form)
                        button.attr("id", ProjectName);
                        button.addClass("submit");
                        button.text("Submit");
                        dynamicdiv.append(button)*/

                        form.append("<br>");

                    }
                    dynamicdiv.append(form)

                }else{
                    dynamicdiv.append("<p>"+ProjectStruct.students[0]+" Has been selected for the project")
                }

            });

            $("#Projects").append(dynamicdiv);
        });
    }


   $(document).on("click",".submit",function () {
       var project=this.id;
       var jsondata = '{'
       jsondata += "\"student_name\":" +"\""+this.name+"\"" + "}";
       console.log(jsondata)

       $.ajax({
           url: 'http://localhost:5000/project/'+project,
          // url: 'http://10.32.58.130:5000/project/'+project,
           type: 'POST',
           data: jsondata,
           contentType:"application/json",
           success: function (result) {
               alert("submitted Successfully");
           },
           error: function (xhr, status, error) {
               alert("Network Conncection Problem!")
           }
       })
    });




});