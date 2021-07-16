var my_vue_app = new Vue({
    el: "#main-app",
    delimiters: ["${", "}"],
    data: {
        // questions_details: {
        //     "id": 1,
        //     "is_edit": false,
        //     "title": "asddsa",
        //     "description": "dasdasdasda",
        //     "topic": "1",
        //     "exercise": "0",
        //     "error": ""
        // },

        questions_details: {
            id: null,
            is_edit: false,
            title: "",
            description: "",
            topic: "",
            exercise: "",
            error: "",
        },

        // list_of_elements : [
        //     {
        //         "key":"MyLabel",
        //         "label": "My Label",
        //         "type": "int",
        //         "nature": "question",
        //         expression_symbol: "a",
        //         example_value: 54,
        //         "is_random": true,
        //         "value": "",
        //         "condition_list": [
        //             {
        //                 "key": ">",
        //                 "value": "greater than",
        //                 "limit": 16
        //             },
        //             {
        //                 "key": "<=",
        //                 "value": "less than equals to",
        //                 "limit": 145
        //             }
        //         ]
        //     },
        //     {
        //         "key": "MyLabel",
        //         "label": "My Label",
        //         "type": "int",
        //         "nature": "question",
        //         expression_symbol: "a",
        //         example_value: 54,
        //         "is_random": true,
        //         "value": "",
        //         "condition_list": [
        //             {
        //                 "key": ">",
        //                 "value": "greater than",
        //                 "limit": 16
        //             },
        //             {
        //                 "key": "<=",
        //                 "value": "less than equals to",
        //                 "limit": 145
        //             }
        //         ]
        //     },
        //     {
        //         "key": "MyLabel",
        //         "label": "My Label",
        //         expression_symbol: "a",
        //         "type": "int",
        //         "nature": "question",
        //         "is_random": true,
        //         "value": "",
        //         example_value: 54,
        //         "condition_list": [
        //             {
        //                 "key": ">",
        //                 "value": "greater than",
        //                 "limit": 16
        //             },
        //             {
        //                 "key": "<=",
        //                 "value": "less than equals to",
        //                 "limit": 145
        //             }
        //         ]
        //     }
        // ],

        list_of_elements: [

        ],

        elements: {
            show_conditions: false,
            is_completed: false,

            types: [
                {
                    key: "int",
                    value: "Integer"
                },
                {
                    key: "double",
                    value: "Double"
                },
                {
                    key: "string",
                    value: "Text"
                },
            ],
            natures: [
                {
                    key: "question",
                    value: "Question (added by teacher)" 
                },
                {
                    key: "answer",
                    value: "Answer (to be added by student)" 
                }
            ],
            condition_compares: [
                {
                    key: ">",
                    value: "greater than"
                },
                {
                    key: ">=",
                    value: "greater than equals to"
                },
                {
                    key: "<",
                    value: "less than"
                },
                {
                    key: "<=",
                    value: "less than equals to"
                },
                {
                    key: "==",
                    value: "equals to"
                },
                {
                    key: "!=",
                    value: "Not equals to"
                }
            ],
            new_condition: {
                code: "",
                condition : "",
                limit: "",
                error: ""
            },

            new_element: {
                label: "",
                type: "",
                nature: "",
                expression_symbol: "",
                example_value: "",
                is_random: false,
                    value: "",
                condition_list: [
                    
                ]
            },
            whole_error: "",
            error: ""
        },


        rules: {
            is_completed: false,
        }
        // is_question_details_edit: false,
        // question_id: 1,
        // question_title: "",
        // question_description: "",
        // question_topic: "",
        // question_exercise: "",
        // question_details_error: "",
    },
    methods: {
        // Rule functions
        is_rules_completed: function () {
            return this.rules.is_completed;
        },

        start_editing_rules: function () {
            return "";  
        },

        save_rule: function () {
            return ""
        },

        set_input_key: function (key) {
            this.rules.expression += key
            $("#demoSource").focus();
        },

        // QUestion details
        save_question_details: function () {
            if (this.questions_details.title && this.questions_details.description) {
                this.questions_details.error = "";
                // this.questions_details.is_edit = false;
                let url = "/save-question";
                let data = {
                    'title': this.questions_details.title,
                    'description':  this.questions_details.description
                }
                if (this.questions_details.is_edit) {
                    data['id'] = this.questions_details.id
                }
                let result = this.get_request(url, data)
                console.log(result);
                if (result['status']) {
                    this.questions_details.id = result['new_question_id'];
                    this.questions_details.is_edit = false;
                }else{
                    this.questions_details.error = "Something went wrong!";
                    this.questions_details.id = null;
                }
            
            }else{
                this.questions_details.error = "Enter all the required information before submission!";
            }
        },

        is_question_details_saved: function () {
            return this.questions_details.id != null && !(this.questions_details.is_edit)
        },

        start_editing_question_details: function () {
            this.questions_details.is_edit = true;
        },

        // Methods for new_element
        toggle_random_value_for_element: function (){
            if (this.elements.new_element.is_random == true) {
                this.elements.new_element.is_random = false
            }else{
                this.elements.new_element.is_random = true
            }
            console.log(this.elements.new_element);
        },

        is_random_allow: function (){
            return this.elements.new_element.is_random;
        },

        is_question: function () {
            return this.elements.new_element.nature == "question";   
        },

        focus: function (id) {
            $(`#${id}`).parent().addClass("active");
        },

        add_element_condition: function () {
            let my_condition = this.elements.new_condition;
            let int_version = parseInt(my_condition.limit);

            if (isNaN(int_version)) {
                this.elements.new_condition.error = "Enter number in the limit input!";
                console.log("value is NaN");
                console.log(this.elements.new_condition.error);
                return false;
            }else{
                this.elements.new_condition.error = "";
            }

            let focused_condition = JSON.stringify(this.elements.condition_compares[my_condition.condition]);
            focused_condition = JSON.parse(focused_condition);
            focused_condition.limit = int_version;
          
            
            for (let i = 0; i < this.elements.new_element.condition_list.length; i++) {
                const single_condition = this.elements.new_element.condition_list[i];
                if (single_condition.value == focused_condition.value) {
                    this.elements.new_element.condition_list.splice(i, 1)
                }
            }

            this.elements.new_element.condition_list.push(
                focused_condition
            );
            this.elements.new_condition = {
                code: "",
                condition : "",
                limit: ""
            }

            console.log(this.elements.new_element.condition_list);
        }, 

        delete_condition: function (index) {
            this.elements.new_element.condition_list.splice(index, 1);
        },

        reset_new_element: function () {
            this.elements.new_element = {
                label: "",
                type: "",
                nature: "",
                is_random: false,
                    value: "",
                condition_list: [
                    
                ]
            }
        },

        copy: function (value) {
            return JSON.parse(JSON.stringify(value));
        },

        is_example_value_required: function(){
            let container = this.elements.new_element;
            return true;
            // if (container.nature == "answer") {
            //     return true;
            // }else{
            //     if (container.is_random) {
            //         return true;
            //     }else{
            //         return false;
            //     }
            // }
        },

        add_element: function () {
            let label = this.elements.new_element.label;
            let type = this.elements.new_element.type;
            let nature = this.elements.new_element.nature;
            let is_random = this.elements.new_element.is_random;
            let condition_list = this.elements.new_element.condition_list;
            let value = this.elements.new_element.value;
            let example_value = this.elements.new_element.example_value;
            let expression_symbol = this.elements.new_element.expression_symbol;
            console.log(this.questions_details);
            console.log(this.list_of_elements);


            if (label && type && nature && expression_symbol && example_value) {
                if ((nature == "answer") || ((is_random && condition_list.length > 0) || (!(is_random) && value))) {
                    this.elements.error = "";
                    let our_data = this.copy(this.elements.new_element);
                    our_data.key = this.make_key(our_data.label);

                    for (let i = 0; i < this.list_of_elements.length; i++) {
                        let single_element = this.list_of_elements[i];
                        if (single_element.key == our_data.key || single_element.expression_symbol == our_data.expression_symbol) {
                            this.elements.error = "This Expression symbol or Label already exists!";
                            return;
                        }
                    }

                    this.list_of_elements.push(
                        our_data
                    );

                    this.reset_new_element()
                    this.elements.whole_error = "";
                    return
                }
            }

            this.elements.error = "Enter all information before submission!";

        },

        is_element_completed: function () {
            return this.elements.is_completed;
        },

        start_editing_element: function () {
            $("#rule-section").hide();
            $("#loop-section").hide();
            $("#success-section").hide();
            this.elements.is_completed = false;
        },

        delete_element: function(element_index){
            this.list_of_elements.splice(element_index, 1);
        },

        make_key: function (input_label) {
            input_label = input_label.replaceAll("_", "");

            let initialize = input_label.split(" ");

            for (let i = 0; i < initialize.length; i++) {
                let element = initialize[i];
                initialize[i] = element[0].toUpperCase() + element.substr(1);
            }

            initialize = initialize.join("");
            return initialize;
            // // initialize = initialize.toLowerCase();
            // var source = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            // let my_key = "";
            // for (i = 0; i < 4; i++){
            //     let number = Math.floor(Math.random() * source.length);
            //     my_key = my_key + source[number];
            // }
            // return initialize + "_" + my_key;
        },

        save_question_elements: function () {

            if (this.list_of_elements.length > 2) {
                this.elements.is_completed = true;    
                let json_list = JSON.stringify(this.list_of_elements)       
                localStorage.setItem("elements", json_list);
                localStorage.setItem("id",  JSON.stringify(this.questions_details.id));

                let data = {
                    'id': this.questions_details.id,
                    'question_element_list': json_list
                }

                let result = this.get_request("/save-question-elements", data)
                if (result['status']) {
                    render_new_elements();
                    $("#rule-section").show();
                    $('html, body').animate({
                        scrollTop: $("#rule-section").offset().top
                    }, 1000);
                }

            }else{
                $("#rule-section").hide();
                localStorage.setItem("elements", JSON.stringify([]));
                this.elements.whole_error = "Add at least 3 elements in the question!";
            }
        },

        to_show_condition_toggle: function () {
            for (let i = 0; i < this.list_of_elements.length; i++) {
                const single_element = this.list_of_elements[i];
                if (single_element.is_random) {
                    let focused_condition_list = single_element.condition_list;
                    if (focused_condition_list.length > 0) {
                        return true
                    }
                }
            }
            return false;
        },

        toggle_show_hide_conditions: function () {
            this.elements.show_conditions = !(this.elements.show_conditions);
        },

        get_request: function (my_url, my_data) {
            let result;
            $.ajax({
                url: my_url,
                type: "GET",
                data: my_data,
                async: false,
                success: function (response) {
                    result = response
                }
            });
            return result;
        }

    },
    filters: {

    },
    created(){
        $("input").each(function () {
            if ($(this).val()) {
                $(this).parent().addClass("active");
            }
        });

        window.MathJax = {
            "fast-preview": {
                       disabled: true
            },
            AuthorInit: function() {
                MathJax.Hub.Register.StartupHook('End', function() {
                    MathJax.Hub.processSectionDelay = 0
                    var demoSource = document.getElementById('demoSource')
                    var demoRendering = document.getElementById('demoRendering')
                    var math = MathJax.Hub.getAllJax('demoRendering')[0]
                    demoSource.addEventListener('input', function() {
                        MathJax.Hub.Queue(['Text', math, demoSource.value])
                    })
                })
            }
        }
    }
});