package com.xclinical.cognito.api;

import io.swagger.annotations.Api;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.stream.Collectors;

@RestController
//@PreAuthorize("hasAuthority('hello_authority')")
@Api(tags = "TokenPayload")
class TokenPayloadController {
    @GetMapping("/access-token-payload-test")
    String info(@AuthenticationPrincipal Jwt principal) {
        return principal.getClaims().keySet().stream()
                .map(key ->
                        formatKeyAndValue(key, String.valueOf(principal.getClaims().get(key)))
                ).collect(Collectors.joining("\n"));
    }

    private String formatKeyAndValue(final String key, final String value) {
        return String.format("%-15s %s", key, value);
    }
}
