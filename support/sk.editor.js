/**
* when click the document . we restore the style of the mouse point's elements 
* just show the action in clicked state 
*/
var signal_product=function(event){
	var target = event.srcElement ;
    _clicked_buttons = "";
    
    while(target){
        if(target.nodeType !== 1){ break; }
        var _tagName = target.tagName.toLowerCase();
        if     ("b"      == _tagName){ _clicked_buttons += "bold,"; }
        else if("s"      == _tagName){ _clicked_buttons += "strikethrough,"; }
        else if("i"      == _tagName){ _clicked_buttons += "italic,"; }
        else if("em"     == _tagName){ _clicked_buttons += "italic,"; }
        else if("ul"     == _tagName){ _clicked_buttons += "unorderedlist,"; }
        else if("ol"     == _tagName){ _clicked_buttons += "orderedlist,"; }
        else if("u"      == _tagName){ _clicked_buttons += "underline,"; }
        else if("sub"    == _tagName){ _clicked_buttons += "subscript,"; }
        else if("sup"    == _tagName){ _clicked_buttons += "superscript,"; }
        else if("h1"     == _tagName){ _clicked_buttons += "h1,"; }
        else if("h2"     == _tagName){ _clicked_buttons += "h2,"; }
        else if("h3"     == _tagName){ _clicked_buttons += "h3,"; }
        
        if(target.style.fontWeight === "bold"){ _clicked_buttons += "bold,"; }
        if(target.style.fontStyle === "bold"){ _clicked_buttons += "italic,"; }
        if(target.style.textAlign === "center"){ _clicked_buttons += "center,"; }
        else if(target.style.textAlign === "left"){ _clicked_buttons += "left,"; }
        else if(target.style.textAlign === "right"){ _clicked_buttons += "right,"; }
        else if(target.style.textAlign === "justify"){ _clicked_buttons += "justify,"; }
        if(target.style.textDecoration === "line-through"){ _clicked_buttons += "strikethrough,"; }
        else if(target.style.textAlign === "underline"){ _clicked_buttons += "underline,"; }
        
        
        //if     ("td"  == _tagName){
        //    wysiwyg.td_clicked_menu(event.clientX,event.clientY);
        //}
        target = target.parentNode;
     }
     wysiwyg.clicked_buttons(_clicked_buttons)
};
document.addEventListener("mouseup",function(event){signal_product(event);},false);
document.addEventListener("keyup",function(event){signal_product(event);},false);
document.addEventListener("click",function(event){signal_product(event);},false);