package com.xclinical.cognito.api;

import io.swagger.annotations.Api;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/messages")
//@PreAuthorize("hasAuthority('hello_authority')")
@Api(tags = "Messages")
class MessagesController {
    @GetMapping("/hello")
    String helloWorld() {
        return "Hello from messages REST API";
    }
}
