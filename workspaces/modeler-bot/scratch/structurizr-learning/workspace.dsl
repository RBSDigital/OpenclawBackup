workspace "Sample Architecture" "Tiny Structurizr DSL sample" {
    model {
        user = person "User" "Uses the system"

        softwareSystem = softwareSystem "Sample System" "Demo system" {
            webApp = container "Web App" "Serves the UI" "React"
            api = container "API" "Provides business logic" "Node.js"
            database = container "Database" "Stores data" "PostgreSQL"
        }

        user -> softwareSystem "Uses"
        webApp -> api "Calls"
        api -> database "Reads from and writes to"
    }

    views {
        systemContext softwareSystem {
            include *
            autolayout lr
        }

        container softwareSystem {
            include *
            autolayout lr
        }
    }
}
