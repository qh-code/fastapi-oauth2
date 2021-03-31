package com.xclinical.cognito;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/messages")
//@PreAuthorize("hasAuthority('hello_authority')")
class MessagesController {
    @GetMapping("/hello")
    @ResponseBody
    String helloWorld() {
        return "Hello from messages REST API";
    }
}
