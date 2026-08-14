workspace {
    model {
        user = person "User" "A user of the system."
        softwareSystem = softwareSystem "Business Software Architecture" "Test system."
        user -> softwareSystem "Uses"
    }
    views {
        systemContext softwareSystem "SystemContext" {
            include *
            autolayout lr
        }
        theme default
    }
}
