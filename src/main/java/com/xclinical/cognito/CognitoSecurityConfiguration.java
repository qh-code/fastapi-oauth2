package com.xclinical.cognito;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.convert.converter.Converter;
import org.springframework.security.authentication.AbstractAuthenticationToken;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.security.oauth2.server.resource.authentication.JwtGrantedAuthoritiesConverter;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Configuration
@EnableWebSecurity
class CognitoSecurityConfiguration extends WebSecurityConfigurerAdapter {

    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/access-token-payload-test")
                        .allowedOrigins("http://localhost:8080")
                        .allowedHeaders("*")
                        .allowedMethods("GET")
                        .allowCredentials(true);
            }
        };
    }

    @Override
    protected void configure(final HttpSecurity http) throws Exception {
        http.authorizeRequests()
                .antMatchers("/v3/api-docs/**", "/swagger-ui.html", "/swagger-ui/**").permitAll()
                .and()
                .cors()
                .and()
                .authorizeRequests()
                .antMatchers("/access-token-payload-test").authenticated()
                .and().csrf().disable()
                .oauth2ResourceServer().jwt()
                .jwtAuthenticationConverter(
                        new GrantedAuthoritiesConverter()
                );
    }

    private static class GrantedAuthoritiesConverter implements Converter<Jwt, AbstractAuthenticationToken> {

        private final JwtGrantedAuthoritiesConverter defaultGrantedAuthoritiesConverter = new JwtGrantedAuthoritiesConverter();

        public GrantedAuthoritiesConverter() {
        }

        @Override
        public AbstractAuthenticationToken convert(final Jwt jwt) {
            Collection<GrantedAuthority> authorities = Stream
                    .concat(defaultGrantedAuthoritiesConverter.convert(jwt).stream(), extractResourceRoles(jwt).stream())
                    .collect(Collectors.toSet());
            return new JwtAuthenticationToken(jwt, authorities);
        }


        public Collection<GrantedAuthority> extractResourceRoles(final Jwt jwt) {
            String claim = "cognito:groups";

            if (jwt.containsClaim(claim)) {
                return jwt.getClaimAsStringList(claim).stream()
                        .map(SimpleGrantedAuthority::new)
                        .collect(Collectors.toUnmodifiableSet());
            }
            return List.of();
        }
    }
}
