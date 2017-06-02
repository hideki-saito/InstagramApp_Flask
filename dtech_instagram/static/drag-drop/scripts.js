// rmodal: replace with external ref
!function(t,o){"object"==typeof exports&&"undefined"!=typeof module?module.exports=o():"function"==typeof define&&define.amd?define(o):t.RModal=o()}(this,function(){var t=function(t,o){return Object.prototype.toString.call(t).toLowerCase()==="[object "+o+"]"},o=function(t,o){var e=t.className.split(/\s+/).filter(function(t){return!!t&&t==o});e.length||(t.className+=" "+o)},e=function(t,o){t.className=t.className.split(/\s+/).filter(function(t){return!!t&&t!=o}).join(" ")},s=function(t,o){var e=this;this.opened=!1,this.opts={bodyClass:"modal-open",dialogClass:"modal-dialog",dialogOpenClass:"bounceInDown",dialogCloseClass:"bounceOutUp",focus:!0,focusElements:["a[href]","area[href]","input:not([disabled]):not([type=hidden])","button:not([disabled])","select:not([disabled])","textarea:not([disabled])","iframe","object","embed","*[tabindex]","*[contenteditable]"],escapeClose:!0,content:null,closeTimeout:500},Object.keys(o||{}).forEach(function(t){void 0!==o[t]&&(e.opts[t]=o[t])}),this.overlay=t,this.dialog=t.querySelector("."+this.opts.dialogClass),this.opts.content&&this.content(this.opts.content)};return s.prototype.open=function(o){var e=this;return this.content(o),t(this.opts.beforeOpen,"function")?void this.opts.beforeOpen(function(){e._doOpen()}):this._doOpen()},s.prototype._doOpen=function(){o(document.body,this.opts.bodyClass),e(this.dialog,this.opts.dialogCloseClass),o(this.dialog,this.opts.dialogOpenClass),this.overlay.style.display="block",this.opts.focus&&(this.focusOutElement=document.activeElement,this.focus()),t(this.opts.afterOpen,"function")&&this.opts.afterOpen(),this.opened=!0},s.prototype.close=function(){var o=this;return t(this.opts.beforeClose,"function")?void this.opts.beforeClose(function(){o._doClose()}):this._doClose()},s.prototype._doClose=function(){var s=this;e(this.dialog,this.opts.dialogOpenClass),o(this.dialog,this.opts.dialogCloseClass),e(document.body,this.opts.bodyClass),this.opts.focus&&this.focus(this.focusOutElement),t(this.opts.afterClose,"function")&&this.opts.afterClose(),this.opened=!1,setTimeout(function(){s.overlay.style.display="none"},this.opts.closeTimeout)},s.prototype.content=function(t){return void 0===t?this.dialog.innerHTML:void(this.dialog.innerHTML=t)},s.prototype.elements=function(o,e){return e=e||window.navigator.appVersion.indexOf("MSIE 9.0")>-1,o=t(o,"array")?o.join(","):o,[].filter.call(this.dialog.querySelectorAll(o),function(t){if(e){var o=window.getComputedStyle(t);return"none"!==o.display&&"hidden"!==o.visibility}return null!==t.offsetParent})},s.prototype.focus=function(o){o=o||this.elements(this.opts.focusElements)[0]||this.dialog.firstChild,o&&t(o.focus,"function")&&o.focus()},s.prototype.keydown=function(t){function o(){t.preventDefault(),t.stopPropagation()}if(this.opts.escapeClose&&27==t.which&&this.close(),this.opened&&9==t.which&&this.dialog.contains(t.target)){var e=this.elements(this.opts.focusElements),s=e[0],i=e[e.length-1];s==i?o():t.target==s&&t.shiftKey?(o(),i.focus()):t.target!=i||t.shiftKey||(o(),s.focus())}},s.prototype.version="1.0.24",s.version="1.0.24",s});

// don't replace the below, it's page-specific:

window.onload = function() {
    var modal = new RModal(document.getElementById('modal'), {
        beforeOpen: function(next) {
            // console.log('beforeOpen');
            next();
        }
        , afterOpen: function() {
            // console.log('opened');
        }

        , beforeClose: function(next) {
            // console.log('beforeClose');
            next();
        }
        , afterClose: function() {
            console.log('closed');
        }
        // , bodyClass: 'modal-open'
        // , dialogClass: 'modal-dialog'
        // , dialogOpenClass: 'animated fadeIn'
        // , dialogCloseClass: 'animated fadeOut'

        // , focus: true
        // , focusElements: ['input.form-control', 'textarea', 'button.btn-primary']

        // , escapeClose: true
    });

    document.addEventListener('keydown', function(ev) {
        modal.keydown(ev);
    }, false);

    document.getElementById('showModal-new').addEventListener("click", function(ev) {
        console.log('new folder')
        ev.preventDefault();
        modal.ourExtensions.makingNewFolder = true;
        modal.open();
    }, false);

    document.getElementById('showModal-rename').addEventListener("click", function(ev) {
        ev.preventDefault();
        modal.ourExtensions.makingNewFolder = false;
        modal.open();
    }, false);

    document.getElementById('delete-images').addEventListener("click", function(ev) {
        ev.preventDefault();
        imageManager.deleteImage();
    }, false);

//    document.getElementById('upload-images').addEventListener("click", function(ev) {
//        ev.preventDefault();
//        imageManager.uploadImage();
//    }, false);


    var imageManager = {
        saveFolderName: function() {
            var newName = document.getElementById('folderName').value;
            var selected = document.querySelector('div.acidjs-css3-treeview input[type="checkbox"]:not([id]):checked');
            if (modal.ourExtensions.makingNewFolder) {
//                if (selected.parentNode.parentNode.className.indexOf('folder') !== -1) {
//                    // folder selected, so add child
//                    imageManager.makeNewNode('folder', selected.parentNode.parentNode.querySelector('ul'), newName);
//                } else {
//                    imageManager.makeNewNode('folder', selected.parentNode.parentNode.querySelector('ul'), newName);
//                    // leaf selected, so add sibling (...for now, do nothing)
//                }
                ajax_functions.create_folder(newName)
            } else {
                if (selected.parentNode.parentNode.className=="folder") {
                    selected.parentNode.nextSibling.innerHTML = newName;
                    ajax_functions.rename(selected.parentNode.parentNode.id, newName, 'folder')
                    }
                else {
                    selected.parentNode.nextSibling.innerHTML = newName;
                    folder_id = selected.parentNode.parentNode.parentNode.parentNode.id
                    ajax_functions.rename(selected.parentNode.parentNode.id, newName, 'leaf')
                }
            }
        },
        makeNewNode: function(type, ul, newName, id) {
            console.log(newName)
            var newNode = document.createElement('li');
            newNode.className = type;
            newNode.id = id
            var newId = "node-" + (new Date() * 1); // unique id
            newNode.innerHTML = '<input type="checkbox" id="' + newId
                + '" /><label><input type="checkbox" /><span></span></label><label ondrop="window.imageManager.drop(event)" ondragover="window.imageManager.allowDrop(event)" draggable="true" ondragstart="window.imageManager.drag(event)" for="' + newId
                + '">' + newName
                + '</label>';

            if (type === 'folder') {
                var newDiv = document.createElement('div');
                newDiv.className = "acidjs-css3-treeview";
                var innerUl = document.createElement('ul');
                newNode.appendChild(innerUl)
                var outerUl = document.createElement('ul')
                outerUl.appendChild(newNode)
                newDiv.appendChild(outerUl)
                ul.appendChild(newDiv);
            }
            else {
                ul.appendChild(newNode);
            }
        },

        deleteImage: function() {
            var selected = document.querySelector('div.acidjs-css3-treeview input[type="checkbox"]:not([id]):checked');
            li = selected.parentNode.parentNode
            if (li.className == 'leaf') {
                ajax_functions.delete_image(li.id, 'leaf')
                li.parentNode.removeChild(li);
                $('.thumbnail>img').attr('src', "");
            } else {
                folder_div = li.parentNode.parentNode
                ajax_functions.delete_image(li.id, 'folder')
                folder_div.parentNode.removeChild(folder_div)
                $('.thumbnail>img').attr('src', "");
            }
        },

        drag: function(ev) {
            ev.dataTransfer.setData("text", "node://" + ev.target.getAttribute('for'));
        },
        allowDrop: function(ev) {
            ev.preventDefault();
        },
        drop: function(ev) {
            ev.preventDefault();
            var parent = ev.target.parentNode;
            if (!parent.querySelector('ul')) { // todo: remove this temp code, only here because of mixed HTML starting point (some folders have ul and some don't)
                parent.appendChild(document.createElement('ul'));
            }
            if (ev.dataTransfer.getData("text").indexOf("node://") === 0) {
                console.log('node')
                var nodeId = ev.dataTransfer.getData("text").substr(7);
                var node = document.getElementById(nodeId).parentNode; // get the li
                node.parentNode.removeChild(node);
                parent.querySelector('ul').appendChild(node);
            } else {
                var data_html = ev.dataTransfer.getData("text/html");
                console.log(data_html)
                data = data_html.split('/');
                data = data[data.length-1]; // just paring down for nicer testing, so it's not the whole url
                name = data.split('.')[0];
                if (name.length > 20) { name = name.substr(0, 20); }
                // todo: check whether image already exists anywhere in the database
                // todo: send to database
                folder = ev.target.parentNode.id
                ajax_functions.save_imageFile(name, folder,  data_html)
            }
        },
    }

    window.imageManager = imageManager;  // we may not need this after making the list dynamic; it's just here for the HTML to be able to refer to it in ondrag, etc.

    modal.ourExtensions = {
        saveFolderName: function(event) {
            imageManager.saveFolderName();
            modal.close();
            event.preventDefault();
        },
        makingNewFolder: false
    }

    window.modal = modal;

    $('body').on('change', 'div.acidjs-css3-treeview input[type="checkbox"]:not([id])', function() {
        if (this.checked) {
            $('div.acidjs-css3-treeview input[type="checkbox"]:not([id]):checked').not(this).prop('checked', false);
        }
    })

    $('body').on('dblclick', '.leaf label:nth-child(3)', function() {
        id = $(this).closest('.leaf').attr('id');
        var url = $SCRIPT_ROOT+"/static/uploads/"+id
        place_image(url)
    })

    $('body').on('click', '.leaf label:nth-child(3)', function() {
        id = $(this).closest('.leaf').attr('id');
        $('.thumbnail>img').attr('src', $SCRIPT_ROOT+"/static/uploads/"+id)
    })

    $('#upload_images').change(function() {
        var selected = document.querySelector('div.acidjs-css3-treeview input[type="checkbox"]:not([id]):checked');
            if (selected) {
                var check_node = selected.parentNode.parentNode
                if (check_node.className == "folder") {
                    folder_id = check_node.id
                    ajax_functions.upload_files(folder_id)
                } else {
                    alert("Select A Folder")
                }
            } else {
                alert("Select A Folder")
            }
    })

    $('.pointer').click(function() {
        var selected = document.querySelector('div.acidjs-css3-treeview input[type="checkbox"]:not([id]):checked');
        if (selected) {
            var check_node = selected.parentNode.parentNode
            if (check_node.className == "folder") {
                var leaf_nodes = check_node.getElementsByTagName('ul')[0].getElementsByTagName('li')
                var image_uris = [];
                for (var i = 0; i < leaf_nodes.length; i++) {
                    image_uris.push(leaf_nodes[i].id);
                }

                var present_uri = $(".thumbnail>img").attr('src').replace($SCRIPT_ROOT+"/static/uploads/", "");
                var present_index = $.inArray(present_uri, image_uris);

                if (this.id == "pointer-preview") {
                    if (present_index==-1 || present_index==image_uris.length-1) {
                        $('.thumbnail>img').attr('src', $SCRIPT_ROOT+"/static/uploads/"+image_uris[0]);
                    } else {
                        $('.thumbnail>img').attr('src', $SCRIPT_ROOT+"/static/uploads/"+image_uris[present_index+1]);
                    }
                } else {
                    if (present_index==-1 || present_index==0) {
                        $('.thumbnail>img').attr('src', $SCRIPT_ROOT+"/static/uploads/"+image_uris[image_uris.length-1]);
                    } else {
                        $('.thumbnail>img').attr('src', $SCRIPT_ROOT+"/static/uploads/"+image_uris[present_index-1]);
                    }
                }
            }
        }
    })

    ajax_functions = {
        save_imageFile: function(name, folder, data, id){
            $.getJSON($SCRIPT_ROOT+'/save_image', {
            name: name,
            folder: folder,
            data: data,
            }, function(data) {
                var uri = data.uri;
                imageManager.makeNewNode('leaf', document.getElementById(folder).querySelector('ul'), name, uri);
            });
        },

        create_folder: function(folder_name){
            $.getJSON($SCRIPT_ROOT+'/create_folder', {
            name: folder_name,
            }, function(data) {
                var id = data.folder_id;
                imageManager.makeNewNode('folder', document.querySelector(".tree"), folder_name, 'folder-'+id);
            });
        },

        rename: function(id, new_name, type) {
            $.getJSON($SCRIPT_ROOT+'/rename', {
            id: id,
            new_name: new_name,
            type: type,
            }, function(data) {
                var response = data.result;
                console.log(response)
            });
        },

        delete_image: function(id, type) {
            $.getJSON($SCRIPT_ROOT+'/delete', {
            id: id,
            type: type,
            }, function(data) {
                var response = data.result;
                console.log(response)
            });
        },

        upload_files: function(folder_id) {
            var form_data = new FormData($('#upload-form')[0]);
            form_data.append('folder_id', folder_id)
            $.ajax({
                type: 'POST',
                url: '/upload_images',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                async: false,
                success: function(data) {
                    console.log(data.uris);
                    console.log(data.names)
                    for (i = 0; i < data.uris.length; i++) {
                        imageManager.makeNewNode('leaf', document.getElementById(folder_id).querySelector('ul'), data.names[i], data.uris[i]);
                    }
                },
            });
        }
    }

}




