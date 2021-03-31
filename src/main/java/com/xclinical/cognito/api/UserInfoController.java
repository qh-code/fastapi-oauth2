package com.xclinical.cognito.api;

import io.swagger.annotations.Api;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collections;
import java.util.Hashtable;
import java.util.Map;

@RestController
@RequestMapping("/api/user")
@Api(tags = "Users")
class UserInfoController {
    @GetMapping("/info")
    public Map<String, Object> getUserInfo(@AuthenticationPrincipal Jwt principal) {
        Map<String, String> map = new Hashtable<>();
//TODO get parameter from claim
//        map.put("user_name", principal.getClaimAsString("preferred_username"));
//        map.put("organization", principal.getClaimAsString("organization"));
        return Collections.unmodifiableMap(map);
    }
}


